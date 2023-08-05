#cython: language_level=3
#cython: boundscheck=False
#cython: wraparound=False

cimport cython
cimport cpython.array
cimport libc.math as math
from libc.stdlib cimport malloc, free
cimport numpy as np

import sys
import numpy as np

import horizont.utils
import horizont._utils


@cython.cdivision(True)
def _sample_topics(int[:] WS, int[:] DS, int[:] ZS, int[:, :] nzw, int[:, :] ndz, int[:] nz,
                   double[:] alpha, double[:] eta, double[:] rands):
    cdef int i, k, w, d, z, z_new, n_topics
    cdef int n_rand = len(rands)
    cdef double r, dist_cum
    cdef double alpha_sum = sum(alpha)
    cdef double eta_sum = sum(eta)
    n_topics = len(nzw)

    cdef double * dist_sum_ptr = <double*> malloc(sizeof(double) * n_topics)
    cdef double[:] dist_sum = <double [:n_topics]> dist_sum_ptr

    for i in range(len(WS)):
        w = WS[i]
        d = DS[i]
        z = ZS[i]

        nzw[z, w] -= 1
        ndz[d, z] -= 1
        nz[z] -= 1

        dist_cum = 0
        for k in range(n_topics):
            # eta is a double so cdivision yields a double
            dist_cum += (nzw[k, w] + eta[w]) / (nz[k] + eta_sum) * (ndz[d, k] + alpha[k])
            dist_sum[k] = dist_cum

        r = rands[i % n_rand] * dist_cum  # dist_cum == dist_sum[-1]
        # XXX: using cimport and a pxd file for searchsorted might be faster
        z_new = horizont._utils.searchsorted(dist_sum, r)

        ZS[i] = z_new
        nzw[z_new, w] += 1
        ndz[d, z_new] += 1
        nz[z_new] += 1

    free(<void *> dist_sum_ptr)


@cython.cdivision(True)
cdef _sample_z(int w, np.ndarray[np.int_t] nz, np.ndarray[np.float_t, ndim=2] Phi, double alpha, r):
    """
    Sample new z given w, nz, and Phi.
    r is a uniform random variate.
    Assumes symmetric Dirichlet.
    """
    n_topics = len(nz)
    probz = np.empty(n_topics)
    for k in range(n_topics):
        probz[k] = Phi[k, w] * nz[k] + alpha
    z_new = horizont._utils.choice(probz, r)
    return z_new


@cython.cdivision(True)
def _score_doc(np.ndarray[np.int_t] x, np.ndarray[np.float_t, ndim=2] Phi,
               double alpha, int R, np.ndarray[np.float_t] rands):
    WS, _ = horizont.utils.matrix_to_lists(np.atleast_2d(x))
    ZS = np.zeros_like(WS)

    n_rand = len(rands)
    i = 0  # index for random draws

    K = len(Phi)
    ll = 0
    for n, w in enumerate(WS):
        pn = 0
        # XXX: tracking just the histogram of topic counts might be faster
        for r in range(R):
            for nprime in range(n):
                r = rands[i % n_rand]
                i += 1
                nz = np.bincount(np.delete(ZS[:n], nprime), minlength=K)
                ZS[nprime] = _sample_z(WS[nprime], nz, Phi, alpha, r)
            nz = np.bincount(ZS[:n], minlength=K)
            Etheta = nz + alpha
            Etheta = 1.0 * Etheta / np.sum(Etheta)
            pn += np.dot(Phi[:, w], Etheta)
        pn = 1.0 * pn / R
        ll += np.log(pn)
    return ll
