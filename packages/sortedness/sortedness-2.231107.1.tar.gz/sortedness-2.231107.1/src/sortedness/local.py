#  Copyright (c) 2023. Davi Pereira dos Santos
#  This file is part of the sortedness project.
#  Please respect the license - more about this in the section (*) below.
#
#  sortedness is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  sortedness is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with sortedness.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#

import gc
from functools import partial
from math import exp

import numpy as np
import pathos.multiprocessing as mp
from numpy import eye, mean, sqrt, ndarray, nan
from numpy.random import permutation
from scipy.spatial.distance import cdist, pdist, squareform
from scipy.stats import rankdata, kendalltau, weightedtau

from sortedness.misc.parallel import rank_alongrow, rank_alongcol


def common(S, S_, i, symmetric, f, isweightedtau, return_pvalues, pmap, kwargs):
    def thread(a, b):
        return f(a, b, **kwargs)

    def oneway(scores_a, scores_b):
        jobs = pmap((thread if kwargs else f), scores_a, scores_b)
        result, pvalues = [], []
        for tup in jobs:
            corr, pvalue = tup if isinstance(tup, tuple) else (tup, nan)
            result.append(corr)
            pvalues.append(pvalue)
        return np.array(result, dtype=float), np.array(pvalues, dtype=float)

    handle_f = lambda tup: tup if isinstance(tup, tuple) else (tup, nan)
    result, pvalues = oneway(S, S_) if i is None else handle_f(f(S, S_, **kwargs))
    if not isweightedtau and symmetric:
        result_, pvalues_ = oneway(S_, S) if i is None else handle_f(f(S_, S, **kwargs))
        result = (result + result_) / 2
        pvalues = (pvalues + pvalues_) / 2

    if return_pvalues:
        return np.array(list(zip(result, pvalues)))
    return result


# todo: see if speed can benefit from:
# gen = pairwise_distances_chunked(X, method='cosine', n_jobs=-1)
# Z = np.concatenate(list(gen), axis=0)
# Z_cond = Z[np.triu_indices(Z.shape[0], k=1)
# https://stackoverflow.com/a/55940399/9681577
#
# import dask.dataframe as dd
# from dask.multiprocessing import get
# # o - is pandas DataFrame
# o['dist_center_from'] = dd.from_pandas(o, npartitions=8).map_partitions(lambda df: df.apply(lambda x: vincenty((x.fromlatitude, x.fromlongitude), center).km, axis=1)).compute(get=get)

def remove_diagonal(X):
    n_points = len(X)
    nI = ~eye(n_points, dtype=bool)  # Mask to remove diagonal.
    return X[nI].reshape(n_points, -1)


weightedtau.isweightedtau = True


def sortedness(X, X_, i=None, symmetric=True, f=weightedtau, return_pvalues=False, parallel=True, parallel_n_trigger=500, parallel_kwargs=None, **kwargs):
    """
     Calculate the sortedness (stress-like correlation-based measure that focuses on ordering of points) value for each point
     Functions available as scipy correlation coefficients:
         ρ-sortedness (Spearman),
         𝜏-sortedness (Kendall's 𝜏),
         w𝜏-sortedness (Sebastiano Vigna weighted Kendall's 𝜏)  ← default

    Note:
        Categorical, or pathological data might present values lower than one due to the presence of ties even with a perfect projection.
        Depending on the chosen correlation coefficient, ties are penalized, as they do not contribute to establishing any order.

    Hint:
        Swap two points A and B at X_ to be able to calculate sortedness between A and B in the same space (i.e., originally, `X = X_`):
            `X = [A, B, C, ..., Z]`
            `X_ = [B, A, C, ..., Z]`
            `sortedness(X, X_, i=0)`

    Parameters
    ----------
    X
        matrix with an instance by row in a given space (often the original one)
    X_
        matrix with an instance by row in another given space (often the projected one)
    i
        None:   calculate sortedness for all instances
        `int`:  index of the instance of interest
    symmetric
        True: Take the mean between extrusion and intrusion emphasis
            Equivalent to `(sortedness(a, b, symmetric=False) + sortedness(b, a, symmetric=False)) / 2` at a slightly lower cost.
            Might increase memory usage.
        False: Weight by original distances (extrusion emphasis), not the projected distances.
    f
        Agreement function:
        callable    =   scipy correlation function:
            weightedtau (weighted Kendall’s τ is the default), kendalltau, spearmanr
            Meaning of resulting values for correlation-based functions:
                1.0:    perfect projection          (regarding order of examples)
                0.0:    random projection           (enough distortion to have no information left when considering the overall ordering)
               -1.0:    worst possible projection   (mostly theoretical; it represents the "opposite" of the original ordering)
    return_pvalues
        For scipy correlation functions, return a 2-column matrix 'corr, pvalue' instead of just 'corr'
        This makes more sense for Kendall's tau. [the weighted version might not have yet a established pvalue calculation method at this moment]
        The null hypothesis is that the projection is random, i.e., sortedness = 0.0.
    parallel
        None: Avoid high-memory parallelization
        True: Full parallelism
        False: No parallelism
    parallel_kwargs
        Any extra argument to be provided to pathos parallelization
    parallel_n_trigger
        Threshold to disable parallelization for small n values
    kwargs
        Arguments to be passed to the correlation measure

     Returns
     -------
         ndarray containing a sortedness value per row, or a single float (include pvalues as a second value if requested)


    >>> ll = [[i] for i in range(17)]
    >>> a, b = np.array(ll), np.array(ll[0:1] + list(reversed(ll[1:])))
    >>> b.ravel()
    array([ 0, 16, 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1])
    >>> r = sortedness(a, b)
    >>> from statistics import median
    >>> round(min(r), 12), round(max(r), 12), round(median(r),12)
    (-1.0, 0.998638259786, 0.937548981983)

    >>> rnd = np.random.default_rng(0)
    >>> rnd.shuffle(ll)
    >>> b = np.array(ll)
    >>> b.ravel()
    array([ 2, 10,  3, 11,  0,  4,  7,  5, 16, 12, 13,  6,  9, 14,  8,  1, 15])
    >>> r = sortedness(a, b)
    >>> r
    array([ 0.24691868, -0.17456491,  0.19184376, -0.18193532,  0.07175694,
            0.27992254,  0.04121859,  0.16249574, -0.03506842,  0.27856259,
            0.40866965, -0.07617887,  0.12184064,  0.24762942, -0.05049511,
           -0.46277399,  0.12193493])
    >>> round(min(r), 12), round(max(r), 12)
    (-0.462773990559, 0.408669653064)
    >>> round(mean(r), 12)
    0.070104521222

    >>> import numpy as np
    >>> from functools import partial
    >>> from scipy.stats import spearmanr, weightedtau
    >>> me = (1, 2)
    >>> cov = eye(2)
    >>> rng = np.random.default_rng(seed=0)
    >>> original = rng.multivariate_normal(me, cov, size=12)
    >>> from sklearn.decomposition import PCA
    >>> projected2 = PCA(n_components=2).fit_transform(original)
    >>> projected1 = PCA(n_components=1).fit_transform(original)
    >>> np.random.seed(0)
    >>> projectedrnd = permutation(original)

    >>> s = sortedness(original, original)
    >>> round(min(s), 12), round(max(s), 12), s
    (1.0, 1.0, array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]))

    # Measure sortedness between two points in the same space.
    >>> M = original.copy()
    >>> M[0], M[1] = original[1], original[0]
    >>> round(sortedness(M, original, 0), 12)
    0.547929184934

    >>> s = sortedness(original, projected2)
    >>> round(min(s), 12), round(max(s), 12), s
    (1.0, 1.0, array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]))
    >>> s = sortedness(original, projected1)
    >>> round(min(s), 12), round(max(s), 12)
    (0.393463224666, 0.944810120534)
    >>> s = sortedness(original, projectedrnd)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.648305479567, 0.397019507592)

    >>> np.round(sortedness(original, original, f=kendalltau, return_pvalues=True), 12)
    array([[1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08],
           [1.0000e+00, 5.0104e-08]])
    >>> sortedness(original, projected2, f=kendalltau)
    array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    >>> sortedness(original, projected1, f=kendalltau)
    array([0.56363636, 0.52727273, 0.81818182, 0.96363636, 0.70909091,
           0.85454545, 0.74545455, 0.92727273, 0.85454545, 0.89090909,
           0.6       , 0.74545455])
    >>> sortedness(original, projectedrnd, f=kendalltau)
    array([ 0.2       , -0.38181818,  0.23636364, -0.09090909, -0.05454545,
            0.23636364, -0.09090909,  0.23636364, -0.63636364, -0.01818182,
           -0.2       , -0.01818182])

    >>> wf = partial(weightedtau, weigher=lambda x: 1 / (x**2 + 1))
    >>> sortedness(original, original, f=wf, return_pvalues=True)
    array([[ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan],
           [ 1., nan]])
    >>> sortedness(original, projected2, f=wf)
    array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    >>> sortedness(original, projected1, f=wf)
    array([0.89469168, 0.89269637, 0.92922928, 0.99721669, 0.86529591,
           0.97806422, 0.94330979, 0.99357377, 0.87959707, 0.92182767,
           0.87256459, 0.87747329])
    >>> sortedness(original, projectedrnd, f=wf)
    array([ 0.23771513, -0.2790059 ,  0.3718005 , -0.16623167,  0.06179047,
            0.40434396, -0.00130294,  0.46569739, -0.67581876, -0.23852189,
           -0.39125007,  0.12131153])
    >>> np.random.seed(14980)
    >>> projectedrnd = permutation(original)
    >>> sortedness(original, projectedrnd)
    array([ 0.24432153, -0.19634576, -0.00238081, -0.4999116 , -0.01625951,
            0.22478766,  0.07176118, -0.48092843,  0.19345964, -0.44895295,
           -0.42044773,  0.06942218])
    >>> sortedness(original, np.flipud(original))
    array([-0.28741742,  0.36769361,  0.06926091,  0.02550202,  0.21424544,
           -0.3244699 , -0.3244699 ,  0.21424544,  0.02550202,  0.06926091,
            0.36769361, -0.28741742])
    >>> original = np.array([[0],[1],[2],[3],[4],[5],[6]])
    >>> projected = np.array([[6],[5],[4],[3],[2],[1],[0]])
    >>> sortedness(original, projected)
    array([1., 1., 1., 1., 1., 1., 1.])
    >>> projected = np.array([[0],[6],[5],[4],[3],[2],[1]])
    >>> sortedness(original, projected)
    array([-1.        ,  0.51956213,  0.81695345,  0.98180162,  0.98180162,
            0.81695345,  0.51956213])
    >>> round(sortedness(original, projected, 1), 12)
    0.519562134793
    >>> round(sortedness(original, projected, 1, symmetric=False), 12)
    0.422638894922
    >>> round(sortedness(projected, original, 1, symmetric=False), 12)
    0.616485374665
    >>> round(sortedness(original, projected, rank=True)[1], 12)
    0.519562134793
    >>> round(sortedness(original, projected, rank=False)[1], 12)  # warning: will consider indexes as ranks!
    0.074070734162
    >>> round(sortedness([[1,2,3,3],[1,2,7,3],[3,4,7,8],[5,2,6,3],[3,5,4,8],[2,7,7,5]], [[7,1,2,3],[3,7,7,3],[5,4,5,6],[9,7,6,3],[2,3,5,1],[1,2,6,3]], 1), 12)
    -1.0
    >>> from scipy.stats import weightedtau
    >>> weightedtau.isweightedtau = False  # warning: will deactivate wau's auto-negativation of scores!
    >>> round(sortedness(original, projected, 1, f=weightedtau, rank=None), 12)
    0.275652884819
    >>> weightedtau.isweightedtau = True
    """
    isweightedtau = False
    if hasattr(f, "isweightedtau") and f.isweightedtau:
        isweightedtau = True
        if not symmetric:
            if "rank" in kwargs:  # pragma: no cover
                raise Exception(f"Cannot set `symmetric=False` and provide `rank` at the same time.")
            kwargs["rank"] = None
    if parallel_kwargs is None:
        parallel_kwargs = {}
    npoints = len(X)

    if i is None:
        tmap = mp.ThreadingPool(**parallel_kwargs).imap if parallel and npoints > parallel_n_trigger else map
        pmap = mp.ProcessingPool(**parallel_kwargs).imap if parallel and npoints > parallel_n_trigger else map
        sqdist_X, sqdist_X_ = tmap(lambda M: cdist(M, M, metric='sqeuclidean'), [X, X_])
        D = remove_diagonal(sqdist_X)
        D_ = remove_diagonal(sqdist_X_)
        scores_X, scores_X_ = (-D, -D_) if isweightedtau else (D, D_)
    else:
        pmap = None
        if not isinstance(X, ndarray):
            X, X_ = np.array(X), np.array(X_)
        x, x_ = X[i], X_[i]
        X = np.delete(X, i, axis=0)
        X_ = np.delete(X_, i, axis=0)
        d_ = np.sum((X_ - x_) ** 2, axis=1)
        d = np.sum((X - x) ** 2, axis=1)
        scores_X, scores_X_ = (-d, -d_) if isweightedtau else (d, d_)

    return common(scores_X, scores_X_, i, symmetric, f, isweightedtau, return_pvalues, pmap, kwargs)


def pwsortedness(X, X_, i=None, symmetric=True, f=weightedtau, parallel=True, parallel_n_trigger=200, batches=10, debug=False, dist=None, cython=False, parallel_kwargs=None, **kwargs):
    """
    Local pairwise sortedness (Λ𝜏w) based on Sebastiano Vigna weighted Kendall's 𝜏

    Importance rankings are calculated internally based on proximity of each pair to the point of interest.

    # TODO?: add flag to break extremely rare cases of ties that persist after projection (implies a much slower algorithm)
        This probably doesn't make any difference on the res, except on categorical, pathological or toy datasets
        Values can be lower due to the presence of ties, but only when the projection isn't prefect for all points.
        In the end, it might be even desired to penalize ties, as they don't exactly contribute to a stronger ordering and are (probabilistically) easier to be kept than a specific order.

    Parameters
    ----------
    X
        Original dataset
    X_
        Projected points
    i
        None:   calculate pwsortedness for all instances
        `int`:  index of the instance of interest
    symmetric
        True: Take the mean between extrusion and intrusion emphasis
            Equivalent to `(pwsortedness(a, b) + pwsortedness(b, a)) / 2` at a slightly lower cost.
            Might increase memory usage.
        False: Weight by original distances (extrusion emphasis), not the projected distances.
    f
        Agreement function that accept the parameter `rank`:
        callable    =   weightedtau (weighted Kendall’s τ is the default) or other compatible correlation function
            Meaning of resulting values for correlation-based functions:
                1.0:    perfect projection          (regarding order of examples)
                0.0:    random projection           (enough distortion to have no information left when considering the overall ordering)
               -1.0:    worst possible projection   (mostly theoretical; it represents the "opposite" of the original ordering)
    parallel
        None: Avoid high-memory parallelization
        True: Full parallelism
        False: No parallelism
    parallel_n_trigger
        Threshold to disable parallelization for small n values
    batches
        Parallel batch size
    debug
        Whether to print more info
    dist
        Provide distance matrices (D, D_) instead of points
        X and X_ should be None
    cython
        Whether to:
            (True) improve speed by ~2x; or,
            (False) be more compatible/portable.
    parallel_kwargs
        Dict of extra arguments to be provided to pathos parallelization
    kwargs
        Any extra argument to be provided to `weightedtau`, e.g., a custom weighting function.
        This only works for `cython=False`.

    Returns
    -------
        Numpy vector or Python float

    >>> import numpy as np
    >>> from functools import partial
    >>> from scipy.stats import spearmanr, weightedtau
    >>> m = (1, 12)
    >>> cov = eye(2)
    >>> rng = np.random.default_rng(seed=0)
    >>> original = rng.multivariate_normal(m, cov, size=12)
    >>> from sklearn.decomposition import PCA
    >>> projected2 = PCA(n_components=2).fit_transform(original)
    >>> projected1 = PCA(n_components=1).fit_transform(original)
    >>> np.random.seed(0)
    >>> projectedrnd = permutation(original)

    >>> r = pwsortedness(original, original)
    >>> min(r), max(r), round(mean(r), 12)
    (1.0, 1.0, 1.0)
    >>> r = pwsortedness(original, projected2)
    >>> min(r), round(mean(r), 12), max(r)
    (1.0, 1.0, 1.0)
    >>> r = pwsortedness(original, projected1)
    >>> min(r), round(mean(r), 12), max(r)
    (0.649315577592, 0.753429143832, 0.834601601062)
    >>> r = pwsortedness(original, projected2[:, 1:])
    >>> min(r), round(mean(r), 12), max(r)
    (0.035312055682, 0.2002329034, 0.352491282966)
    >>> r = pwsortedness(original, projectedrnd)
    >>> min(r), round(mean(r), 12), max(r)
    (-0.168611098044, -0.079882538998, 0.14442446342)
    >>> round(pwsortedness(original, projected1)[1], 12)
    0.649315577592
    >>> round(pwsortedness(original, projected1, cython=True)[1], 12)
    0.649315577592
    >>> round(pwsortedness(original, projected1, i=1), 12)
    0.649315577592
    >>> round(pwsortedness(original, projected1, symmetric=False, cython=True)[1], 12)
    0.730078995423
    >>> round(pwsortedness(original, projected1, symmetric=False, i=1), 12)
    0.730078995423
    >>> np.round(pwsortedness(original, projected1, symmetric=False), 12)
    array([0.75892647, 0.730079  , 0.83496865, 0.73161226, 0.75376525,
           0.83301104, 0.76695755, 0.74759156, 0.81434161, 0.74067221,
           0.74425225, 0.83731035])
    >>> np.round(pwsortedness(original, projected1, f=weightedtau, symmetric=False), 12)
    array([0.75892647, 0.730079  , 0.83496865, 0.73161226, 0.75376525,
           0.83301104, 0.76695755, 0.74759156, 0.81434161, 0.74067221,
           0.74425225, 0.83731035])
    >>> np.round(pwsortedness(original, projected1, f=weightedtau, symmetric=False, weigher=hyperbolic), 12)
    array([0.75892647, 0.730079  , 0.83496865, 0.73161226, 0.75376525,
           0.83301104, 0.76695755, 0.74759156, 0.81434161, 0.74067221,
           0.74425225, 0.83731035])
    >>> np.round(pwsortedness(original, projected1, f=weightedtau, symmetric=False, weigher=gaussian), 12)
    array([0.74141933, 0.71595198, 0.94457495, 0.72528033, 0.78637383,
           0.92562531, 0.77600408, 0.74811014, 0.87241023, 0.8485321 ,
           0.82264118, 0.95322218])
    """
    if "rank" in kwargs:  # pragma: no cover
        raise Exception(f"Cannot provide `rank` as kwarg for pwsortedness. The pairwise distances ranking is calculated internally.")
    isweightedtau = hasattr(f, "isweightedtau") and f.isweightedtau
    if parallel_kwargs is None:
        parallel_kwargs = {}
    if cython and (kwargs or not isweightedtau):  # pragma: no cover
        raise Exception(f"Cannot provide custom `f` or `f` kwargs with `cython=True`")
    npoints = len(X) if X is not None else len(dist[0])  # pragma: no cover
    tmap = mp.ThreadingPool(**parallel_kwargs).imap if parallel and npoints > parallel_n_trigger else map
    pmap = mp.ProcessingPool(**parallel_kwargs).imap if parallel and npoints > parallel_n_trigger else map
    thread = lambda M: pdist(M, metric="sqeuclidean")
    scores_X, scores_X_ = tmap(thread, [X, X_]) if X is not None else (squareform(dist[0]), squareform(dist[1]))
    if isweightedtau:
        scores_X, scores_X_ = -scores_X, -scores_X_

    def makeM(E):
        n = len(E)
        m = (n ** 2 - n) // 2
        M = np.zeros((m, E.shape[1]))
        c = 0
        for i in range(n - 1):  # a bit slow, but only a fraction of wtau (~5%)
            h = n - i - 1
            d = c + h
            M[c:d] = E[i] + E[i + 1:]
            c = d
        del E
        gc.collect()
        return M.T

    if symmetric:
        D, D_ = tmap(squareform, [-scores_X, -scores_X_]) if dist is None else (dist[0], dist[1])
    else:
        D = squareform(-scores_X) if dist is None else dist[0]

    if i is None:
        n = len(D)
        if symmetric:
            M, M_ = pmap(makeM, [D, D_])
            R_ = rank_alongrow(M_, step=n // batches, parallel=parallel, **parallel_kwargs).T
            del M_
        else:
            M = makeM(D)
        R = rank_alongrow(M, step=n // batches, parallel=parallel, **parallel_kwargs).T
        del M
        gc.collect()
        if cython:
            from sortedness.wtau import parwtau
            res = parwtau(scores_X, scores_X_, npoints, R, parallel=parallel, **parallel_kwargs)
            del R
            if not symmetric:
                gc.collect()
                return res

            res_ = parwtau(scores_X, scores_X_, npoints, R_, parallel=parallel, **parallel_kwargs)
            del R_
            gc.collect()
            return (res + res_) / 2
        else:
            def thread(r):
                corr = f(scores_X, scores_X_, rank=r, **kwargs)[0]
                return corr

            gen = (R[:, i] for i in range(len(X)))
            res = np.array(list(pmap(thread, gen)), dtype=float)
            del R
            if not symmetric:
                gc.collect()
                return res

            gen = (R_[:, i] for i in range(len(X_)))
            res_ = np.array(list(pmap(thread, gen)), dtype=float)
            del R_
            gc.collect()
            return np.round((res + res_) / 2, 12)

    if symmetric:
        M, M_ = pmap(makeM, [D[:, i:i + 1], D_[:, i:i + 1]])
        thread = lambda M: rankdata(M, axis=1, method="average")
        r, r_ = [r[0].astype(int) - 1 for r in tmap(thread, [M, M_])]  # todo: asInt and method="average" does not play nicely together  for ties!!
        s1 = f(scores_X, scores_X_, r, **kwargs)[0]
        s2 = f(scores_X, scores_X_, r_, **kwargs)[0]
        return round((s1 + s2) / 2, 12)

    M = makeM(D[:, i:i + 1])
    r = rankdata(M, axis=1, method="average")[0].astype(int) - 1
    return round(f(scores_X, scores_X_, r, **kwargs)[0], 12)


def rsortedness(X, X_, i=None, symmetric=True, f=weightedtau, return_pvalues=False, parallel=True, parallel_n_trigger=500, parallel_kwargs=None, **kwargs):  # pragma: no cover
    """
    Reciprocal sortedness: consider the neighborhood relation the other way around

    Might be good to assess the effect of a projection on hubness, and also to serve as a loss function for a custom projection algorithm.

    WARNING: this function is experimental, i.e., not as well tested as the others; it might need a better algorithm/fomula as well.

    # TODO?: add flag to break (not so rare) cases of ties that persist after projection (implies a much slower algorithm)
        This probably doesn't make any difference on the result, except on categorical, pathological or toy datasets
        Values can be lower due to the presence of ties, but only when the projection isn't prefect for all points.
        In the end, it might be even desired to penalize ties, as they don't exactly contribute to a stronger ordering and are (probabilistically) easier to be kept than a specific order.

    Parameters
    ----------
    X
        Original dataset
    X_
        Projected points
    i
        None:   calculate rsortedness for all instances
        `int`:  index of the instance of interest
    symmetric
        True: Take the mean between extrusion and intrusion emphasis
            Equivalent to `(rsortedness(a, b) + rsortedness(b, a)) / 2` at a slightly lower cost.
            Might increase memory usage.
        False: Weight by original distances (extrusion emphasis), not the projected distances.
    f
        Agreement function:
        callable    =   scipy correlation function:
            weightedtau (weighted Kendall’s τ is the default), kendalltau, spearmanr
            Meaning of resulting values for correlation-based functions:
                1.0:    perfect projection          (regarding order of examples)
                0.0:    random projection           (enough distortion to have no information left when considering the overall ordering)
               -1.0:    worst possible projection   (mostly theoretical; it represents the "opposite" of the original ordering)
    return_pvalues
        For scipy correlation functions, return a 2-column matrix 'corr, pvalue' instead of just 'corr'
        This makes more sense for Kendall's tau. [the weighted version might not have yet a established pvalue calculation method at this moment]
        The null hypothesis is that the projection is random, i.e., sortedness = 0.0.
    parallel
        None: Avoid high-memory parallelization
        True: Full parallelism
        False: No parallelism
    parallel_kwargs
        Any extra argument to be provided to pathos parallelization
    parallel_n_trigger
        Threshold to disable parallelization for small n values
    kwargs
        Arguments to be passed to the correlation measure

    Returns
    -------
        Numpy vector

    >>> ll = [[i] for i in range(17)]
    >>> a, b = np.array(ll), np.array(ll[0:1] + list(reversed(ll[1:])))
    >>> b.ravel()
    array([ 0, 16, 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1])
    >>> r = rsortedness(a, b)
    >>> round(min(r), 12), round(max(r), 12)
    (-0.707870893072, 0.961986592073)

    >>> rnd = np.random.default_rng(1)
    >>> rnd.shuffle(ll)
    >>> b = np.array(ll)
    >>> b.ravel()
    array([ 1, 10, 14, 15,  7, 12,  3,  4,  5,  8,  0,  9,  2, 16, 13, 11,  6])
    >>> r = rsortedness(a, b)
    >>> np.round(r, 12)
    array([-0.38455603, -0.28634813,  0.23902905,  0.19345863, -0.43727482,
           -0.3498781 ,  0.29240532,  0.52016504,  0.51878015,  0.07744892,
           -0.03664284, -0.17163371, -0.16346701, -0.07260407, -0.03677776,
            0.00183332, -0.25692691])
    >>> round(min(r), 12), round(max(r), 12)
    (-0.437274823593, 0.520165040078)
    >>> round(mean(r), 12)
    -0.020764055466

    >>> import numpy as np
    >>> from functools import partial
    >>> from scipy.stats import spearmanr, weightedtau
    >>> me = (1, 2)
    >>> cov = eye(2)
    >>> rng = np.random.default_rng(seed=10)
    >>> original = rng.multivariate_normal(me, cov, size=30)
    >>> from sklearn.decomposition import PCA
    >>> projected2 = PCA(n_components=2).fit_transform(original)
    >>> projected1 = PCA(n_components=1).fit_transform(original)
    >>> np.random.seed(10)
    >>> projectedrnd = permutation(original)

    >>> s = rsortedness(original, original)
    >>> round(min(s), 12), round(max(s), 12)
    (1.0, 1.0)
    >>> s = rsortedness(original, projected2)
    >>> round(min(s), 12), round(max(s), 12)
    (1.0, 1.0)
    >>> s = rsortedness(original, projected1)
    >>> round(min(s), 12), round(max(s), 12)
    (0.160980548632, 0.967351026423)
    >>> s = rsortedness(original, projectedrnd)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.406104443754, 0.427134084097)
    >>> s = rsortedness(original, original, f=kendalltau, return_pvalues=True)
    >>> np.round(s.min(axis=0), 12), np.round(s.max(axis=0), 12)
    (array([1., 0.]), array([1.00e+00, 3.58e-10]))
    >>> s = rsortedness(original, projected2, f=kendalltau)
    >>> round(min(s), 12), round(max(s), 12)
    (1.0, 1.0)
    >>> s = rsortedness(original, projected1, f=kendalltau)
    >>> round(min(s), 12), round(max(s), 12)
    (0.045545155427, 0.920252656485)
    >>> s = rsortedness(original, projectedrnd, f=kendalltau)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.302063337022, 0.306710199121)
    >>> wf = partial(weightedtau, weigher=lambda x: 1 / (x**2 + 1))
    >>> s = rsortedness(original, original, f=wf, return_pvalues=True)
    >>> np.round(s.min(axis=0), 12), np.round(s.max(axis=0), 12)
    (array([ 1., nan]), array([ 1., nan]))
    >>> s = rsortedness(original, projected2, f=wf)
    >>> round(min(s), 12), round(max(s), 12)
    (1.0, 1.0)
    >>> s = rsortedness(original, projected1, f=wf)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.119320940022, 0.914184310816)
    >>> s = rsortedness(original, projectedrnd, f=wf)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.418929560486, 0.710828808816)
    >>> np.random.seed(14980)
    >>> projectedrnd = permutation(original)
    >>> s = rsortedness(original, projectedrnd)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.415049518972, 0.465004321022)
    >>> s = rsortedness(original, np.flipud(original))
    >>> round(min(s), 12), round(max(s), 12)
    (-0.258519523874, 0.454184518962)
    >>> original = np.array([[0],[1],[2],[3],[4],[5],[6]])
    >>> projected = np.array([[6],[5],[4],[3],[2],[1],[0]])
    >>> s = rsortedness(original, projected)
    >>> round(min(s), 12), round(max(s), 12)
    (1.0, 1.0)
    >>> projected = np.array([[0],[6],[5],[4],[3],[2],[1]])
    >>> s = rsortedness(original, projected)
    >>> round(min(s), 12), round(max(s), 12)
    (-0.755847611802, 0.872258373962)
    >>> round(rsortedness(original, projected, 1), 12)
    0.544020048033
    >>> round(rsortedness(original, projected, 1, symmetric=False), 12)
    0.498125132865
    >>> round(rsortedness(projected, original, 1, symmetric=False), 12)
    0.589914963202
    >>> round(rsortedness(original, projected, rank=True)[1], 12)
    0.544020048033
    >>> round(rsortedness(original, projected, rank=False)[1], 12) # warning: will consider indexes as ranks!
    0.208406304729
    >>> round(rsortedness([[1,2,3,3],[1,2,7,3],[3,4,7,8],[5,2,6,3],[3,5,4,8],[2,7,7,5]], [[7,1,2,3],[3,7,7,3],[5,4,5,6],[9,7,6,3],[2,3,5,1],[1,2,6,3]], 1), 12)
    -0.294037071368
    >>> from scipy.stats import weightedtau
    >>> weightedtau.isweightedtau = False  # warning: will deactivate wau's auto-negativation of scores!
    >>> round(rsortedness(original, projected, 1, f=weightedtau, rank=None), 12)
    0.483816220002
    >>> weightedtau.isweightedtau = True

    """
    isweightedtau = False
    if hasattr(f, "isweightedtau") and f.isweightedtau:
        isweightedtau = True
        if not symmetric:
            if "rank" in kwargs:
                raise Exception(f"Cannot set `symmetric=False` and provide `rank` at the same time.")
            kwargs["rank"] = None
    if parallel_kwargs is None:
        parallel_kwargs = {}
    npoints = len(X)
    tmap = mp.ThreadingPool(**parallel_kwargs).imap if parallel and npoints > parallel_n_trigger else map
    pmap = mp.ProcessingPool(**parallel_kwargs).imap if parallel and npoints > parallel_n_trigger else map
    D, D_ = tmap(lambda M: cdist(M, M, metric="sqeuclidean"), [X, X_])
    R, R_ = (rank_alongcol(M, parallel=parallel) for M in [D, D_])
    scores_X, scores_X_ = tmap(lambda M: remove_diagonal(M), [R, R_])
    if isweightedtau:
        scores_X, scores_X_ = -scores_X, -scores_X_

    if hasattr(f, "isparwtau"):  # pragma: no cover
        raise Exception("TODO: Pairtau implementation disagree with scipy weightedtau")
        # return parwtau(scores_X, scores_X_, npoints, parallel=parallel, **kwargs)
    if i is not None:
        scores_X, scores_X_ = scores_X[i], scores_X_[i]
    return common(scores_X, scores_X_, i, symmetric, f, isweightedtau, return_pvalues, pmap, kwargs)


def stress(X, X_, i=None, metric=True, parallel=True, parallel_n_trigger=10000, **parallel_kwargs):
    """
    Kruskal's "Stress Formula 1" normalized before comparing distances.
    default: Euclidean

    Parameters
    ----------
    X
        matrix with an instance by row in a given space (often the original one)
    X_
        matrix with an instance by row in another given space (often the projected one)
    i
        None:   calculate stress for all instances
        `int`:  index of the instance of interest
    metric
        Stress formula version: metric or nonmetric
    parallel
        Parallelize processing when |X|>1000. Might use more memory.

    Returns
    -------
    parallel_kwargs
        Any extra argument to be provided to pathos parallelization
    parallel_n_trigger
        Threshold to disable parallelization for small n values

    >>> import numpy as np
    >>> from functools import partial
    >>> from scipy.stats import spearmanr, weightedtau
    >>> mean = (1, 12)
    >>> cov = eye(2)
    >>> rng = np.random.default_rng(seed=0)
    >>> original = rng.multivariate_normal(mean, cov, size=12)
    >>> original
    array([[ 1.12573022, 11.86789514],
           [ 1.64042265, 12.10490012],
           [ 0.46433063, 12.36159505],
           [ 2.30400005, 12.94708096],
           [ 0.29626476, 10.73457853],
           [ 0.37672554, 12.04132598],
           [-1.32503077, 11.78120834],
           [-0.24591095, 11.26773265],
           [ 0.45574102, 11.68369984],
           [ 1.41163054, 13.04251337],
           [ 0.87146534, 13.36646347],
           [ 0.33480533, 12.35151007]])
    >>> s = stress(original, original*5)
    >>> round(min(s), 12), round(max(s), 12), s
    (0.0, 0.0, array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
    >>> from sklearn.decomposition import PCA
    >>> projected = PCA(n_components=2).fit_transform(original)
    >>> s = stress(original, projected)
    >>> round(min(s), 12), round(max(s), 12), s
    (0.0, 0.0, array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
    >>> projected = PCA(n_components=1).fit_transform(original)
    >>> s = stress(original, projected)
    >>> round(min(s), 12), round(max(s), 12), s
    (0.073383317103, 0.440609121637, array([0.26748441, 0.31603101, 0.24636389, 0.07338332, 0.34571508,
           0.19548442, 0.1800883 , 0.16544039, 0.2282494 , 0.16405274,
           0.44060912, 0.27058614]))
    >>> stress(original, projected)
    array([0.26748441, 0.31603101, 0.24636389, 0.07338332, 0.34571508,
           0.19548442, 0.1800883 , 0.16544039, 0.2282494 , 0.16405274,
           0.44060912, 0.27058614])
    >>> stress(original, projected, metric=False)
    array([0.36599664, 0.39465927, 0.27349092, 0.25096851, 0.31476019,
           0.27612935, 0.3064739 , 0.26141414, 0.2635681 , 0.25811772,
           0.36113025, 0.29740821])
    >>> stress(original, projected, 1)
    0.316031007598
    >>> stress(original, projected, 1, metric=False)
    0.39465927169
    """
    tmap = mp.ThreadingPool(**parallel_kwargs).imap if parallel and X.size > parallel_n_trigger else map
    # TODO: parallelize cdist in slices?
    if metric:
        thread = (lambda M, m: cdist(M, M, metric=m)) if i is None else (lambda M, m: cdist(M[i:i + 1], M, metric=m))
        D, Dsq_ = tmap(thread, [X, X_], ["Euclidean", "sqeuclidean"])
        Dsq_ /= Dsq_.max(axis=1, keepdims=True)
        D_ = sqrt(Dsq_)
    else:
        thread = (lambda M, m: rankdata(cdist(M, M, metric=m), method="average", axis=1) - 1) if i is None else (lambda M, m: rankdata(cdist(M[i:i + 1], M, metric=m), method="average", axis=1) - 1)
        D, Dsq_ = tmap(thread, [X, X_], ["Euclidean", "sqeuclidean"])
        Dsq_ /= Dsq_.max(axis=1, keepdims=True)
        D_ = sqrt(Dsq_)

    D /= D.max(axis=1, keepdims=True)
    s = ((D - D_) ** 2).sum(axis=1) / 2
    result = np.round(np.sqrt(s / (Dsq_.sum(axis=1) / 2)), 12)
    return result if i is None else result.flat[0]


def hyperbolic(x):
    """
    >>> import numpy as np
    >>> np.round(list(map(hyperbolic, range(10))), 12).tolist()
    [1.0, 0.5, 0.333333333333, 0.25, 0.2, 0.166666666667, 0.142857142857, 0.125, 0.111111111111, 0.1]
    """
    return 1 / (1 + x)


def hyperbolic_np(x):
    """
    >>> import numpy as np
    >>> np.round(hyperbolic_np(list(range(10))), 12).tolist()
    [1.0, 0.5, 0.333333333333, 0.25, 0.2, 0.166666666667, 0.142857142857, 0.125, 0.111111111111, 0.1]
    """
    return np.divide(1, np.add(1, x))


def gaussian(x, ampl=1., sigma=1.):
    """
    >>> import numpy as np
    >>> np.round(list(map(gaussian, range(10))), 12).tolist()
    [1.0, 0.606530659713, 0.135335283237, 0.011108996538, 0.000335462628, 3.726653e-06, 1.523e-08, 2.3e-11, 0.0, 0.0]
    """
    return ampl * exp(- (x / sigma) ** 2 / 2)


def gaussian_np(x, ampl=1., sigma=1.):
    """
    >>> import numpy as np
    >>> np.round(gaussian_np(list(range(10))), 12).tolist()
    [1.0, 0.606530659713, 0.135335283237, 0.011108996538, 0.000335462628, 3.726653e-06, 1.523e-08, 2.3e-11, 0.0, 0.0]
    """
    return ampl * np.exp(- np.divide(x, sigma) ** 2 / 2)
