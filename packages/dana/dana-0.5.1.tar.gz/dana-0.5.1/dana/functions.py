#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright INRIA
# Contributors: Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
#
# DANA is a computing framework for the simulation of distributed,
# asynchronous, numerical and adaptive models.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info/index.en.html.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# -----------------------------------------------------------------------------
""" Some useful functions """
import numpy as np
import scipy.linalg
import scipy.sparse as sp
from scipy.ndimage.filters import convolve
from group import Group

def best_fft_shape(shape):
    """
    From fftw.org:
        FFTW is best at handling sizes of the form 2^a*3^b*5^c*7^d*11^e*13^f,
         where e+f is either 0 or 1,

    This function finds the best shape for computing fftw
    """

    base = [13,11,7,5,3,2]

    def factorize(n):
        if not n:
            raise(RuntimeError, "Length n must be positive integer")
        elif n == 1:
            return [1,]
        factors = []
        for b in base:
            while n % b == 0:
                n /= b
                factors.append(b)
        if n == 1:
            return factors
        return []

    def is_optimal(n):
        factors = factorize(n)
        return len(factors) > 0 \
            and factors[:2] not in [[13,13],[13,11],[11,11]]

    shape = np.atleast_1d(np.array(shape))
    for i in range(shape.size):
        while not is_optimal(shape[i]):
            shape[i] += 1
    return shape.astype(int)



def convolve1d(Z, K, toric=False):
    """ Discrete, clamped, linear convolution of two one-dimensional sequences.

        The convolution operator is often seen in signal processing, where it
        models the effect of a linear time-invariant system on a signal [1]_.
        In probability theory, the sum of two independent random variables is
        distributed according to the convolution of their individual
        distributions.
    
        :param array Z:
            One-dimensional array.
        :param array K:
            One-dimensional array.
        :param bool toric:
            Indicate whether convolution should be considered toric
        :return: 
            Discrete, clamped, linear convolution of `Z` and `K`.

        **Note**

            The discrete convolution operation is defined as

            .. math:: (f * g)[n] = \sum_{m = -\infty}^{\infty} f[m] g[n-m]

        **References**

        .. [1] Wikipedia, "Convolution",
                      http://en.wikipedia.org/wiki/Convolution.
    """

    if toric:
        return convolve(Z,K,mode='wrap')
    else:
        return convolve(Z,K,mode='constant')

    #return convolve(Z,K,mode='wrap')
    # R = np.convolve(Z, K, 'same')
    # i0 = 0
    # if R.shape[0] > Z.shape[0]:
    #     i0 = (R.shape[0]-Z.shape[0])/2 + 1 - Z.shape[0]%2
    # i1 = i0+ Z.shape[0]
    # return R[i0:i1]



def convolve2d(Z, K, USV = None, toric=False):
    """ Discrete, clamped convolution of two two-dimensional arrays.

        The convolution operator is often seen in signal processing, where it
        models the effect of a linear time-invariant system on a signal [1]_.
        In probability theory, the sum of two independent random variables is
        distributed according to the convolution of their individual
        distributions. If the kernel K is separable, it is decomposed using a
        singular value decomposition [2]_ and the computing is optimized
        accordingly (when rank n is inferior to S.size/2)
    

        :param array Z:
            Two-dimensional array.
        :param array K:
            Two-dimensional array.
        :param tuple USV
            (U,S,V) as a result of scipy.linalg.svd(K).
        :param bool toric:
            Indicate whether convolution should be considered toric
        :return: 
            Discrete, clamped, linear convolution of `Z` and `K`.

        **Note**

            The discrete convolution operation is defined as

            .. math:: (f * g)[n] = \sum_{m = -\infty}^{\infty} f[m] g[n-m]

        **References**

        .. [1] Wikipedia, "Convolution",
                  http://en.wikipedia.org/wiki/Convolution.
        .. [2] Wikipedia, "Singular Value Decomposition",
                  http://en.wikipedia.org/wiki/Singular_value_decomposition."
    """

    if USV is None:
        U,S,V = scipy.linalg.svd(K)
        U,S,V = U.astype(K.dtype), S.astype(K.dtype), V.astype(K.dtype)
    else:
        U,S,V = USV
    n = (S > 1e-12).sum()
#    n = (S > 0).sum()
    R = np.zeros( Z.shape )
    for k in range(n):
        Zt = Z.copy() * S[k]
        for i in range(Zt.shape[0]):
            Zt[i,:] = convolve1d(Zt[i,:], V[k,::-1], toric)
        for i in range(Zt.shape[1]):
            Zt[:,i] = convolve1d(Zt[:,i], U[::-1,k], toric)
        R += Zt
    return R



def extract(Z, shape, position, fill=0):
    """ Extract a sub-array from Z using given shape and centered on position.
        If some part of the sub-array is out of Z bounds, result will be padded
        with fill value.

        **Parameters**
            `Z` : array_like
               Input array.

           `shape` : tuple
               Shape of the output array

           `position` : tuple
               Position within Z

           `fill` : scalar
               Fill value

        **Returns**
            `out` : array_like
                Z slice with given shape and center

        **Examples**

        >>> Z = np.arange(0,16).reshape((4,4))
        >>> extract(Z, shape=(3,3), position=(0,0))
        [[ NaN  NaN  NaN]
         [ NaN   0.   1.]
         [ NaN   4.   5.]]

        Schema:

            +-----------+
            | 0   0   0 | = extract (Z, shape=(3,3), position=(0,0))
            |   +---------------+
            | 0 | 0   1 | 2   3 | = Z
            |   |       |       |
            | 0 | 4   5 | 6   7 |
            +---|-------+       |
                | 8   9  10  11 |
                |               |
                | 12 13  14  15 |
                +---------------+

        >>> Z = np.arange(0,16).reshape((4,4))
        >>> extract(Z, shape=(3,3), position=(3,3))
        [[ 10.  11.  NaN]
         [ 14.  15.  NaN]
         [ NaN  NaN  NaN]]

        Schema:

            +---------------+
            | 0   1   2   3 | = Z
            |               |
            | 4   5   6   7 |
            |       +-----------+
            | 8   9 |10  11 | 0 | = extract (Z, shape=(3,3), position=(3,3))
            |       |       |   |
            | 12 13 |14  15 | 0 |
            +---------------+   |
                    | 0   0   0 |
                    +-----------+
    """
#    assert(len(position) == len(Z.shape))
#    if len(shape) < len(Z.shape):
#        shape = shape + Z.shape[len(Z.shape)-len(shape):]

    R = np.ones(shape, dtype=Z.dtype)*fill
    P  = np.array(list(position)).astype(int)
    Rs = np.array(list(R.shape)).astype(int)
    Zs = np.array(list(Z.shape)).astype(int)

    R_start = np.zeros((len(shape),)).astype(int)
    R_stop  = np.array(list(shape)).astype(int)
    Z_start = (P-Rs//2)
    Z_stop  = (P+Rs//2)+Rs%2

    R_start = (R_start - np.minimum(Z_start,0)).tolist()
    Z_start = (np.maximum(Z_start,0)).tolist()
    #R_stop = (R_stop - np.maximum(Z_stop-Zs,0)).tolist()
    R_stop = np.maximum(R_start, (R_stop - np.maximum(Z_stop-Zs,0))).tolist()
    Z_stop = (np.minimum(Z_stop,Zs)).tolist()

    r = [slice(start,stop) for start,stop in zip(R_start,R_stop)]
    z = [slice(start,stop) for start,stop in zip(Z_start,Z_stop)]

    R[r] = Z[z]

    return R



def convolution_matrix(src, dst, kernel, toric=False):
    """
    Build a sparse convolution matrix M such that:

    (M*src.ravel()).reshape(src.shape) = convolve2d(src,kernel)

    You can specify whether convolution is toric or not and specify a different
    output shape. If output (dst) is different, convolution is only applied at
    corresponding normalized location within the src array.

    Building the matrix can be pretty long if your kernel is big but it can
    nonetheless saves you some time if you need to apply several convolution
    compared to fft convolution (no need to go to the Fourier domain).

    Parameters:
    -----------

    src : n-dimensional numpy array
        Source shape

    dst : n-dimensional numpy array
        Destination shape

    kernel : n-dimensional numpy array
        Kernel to be used for convolution

    Returns:
    --------

    A sparse convolution matrix

    Examples:
    ---------

    >>> Z = np.ones((3,3))
    >>> M = convolution_matrix(Z,Z,Z,True)
    >>> print (M*Z.ravel()).reshape(Z.shape)
    [[ 9.  9.  9.]
     [ 9.  9.  9.]
     [ 9.  9.  9.]]
    >>> M = convolution_matrix(Z,Z,Z,False)
    >>> print (M*Z.ravel()).reshape(Z.shape)
    [[ 4.  6.  4.]
     [ 6.  9.  6.]
     [ 4.  6.  4.]]
    """
 
    # For a toric connection, it is wrong to have a kernel larger
    # than the source
 #   if toric:
 #       shape = np.minimum(np.array(src.shape), np.array(kernel.shape))
 #       kernel = extract(kernel, shape, np.rint(np.array(kernel.shape)/2.))

    # Get non NaN value from kernel and their indices.
    nz = (1 - np.isnan(kernel)).nonzero()
    data = kernel[nz].ravel()
    indices = [0,]*(len(kernel.shape)+1)
    indices[0] = np.array(nz)
    indices[0] += np.atleast_2d((np.array(src.shape)//2 - np.array(kernel.shape)//2)).T

    # Generate an array A for a given shape such that given an index tuple I,
    # we can translate into a flat index F = (I*A).sum()
    to_flat_index = np.ones((len(src.shape),1), dtype=int)
    if len(src.shape) > 1:
        to_flat_index[:-1] = src.shape[1]

    R, C, D = [], [], []
    dst_index = 0
    src_indices = []

    # Translate target tuple indices into source tuple indices taking care of
    # possible scaling (this is done by normalizing indices)
    for i in range(len(src.shape)):
        z = np.rint((np.linspace(0,1,dst.shape[i])*(src.shape[i]-1))).astype(int)
        src_indices.append(z)

    nd = [0,]*(len(kernel.shape))
    for index in np.ndindex(dst.shape):
        dims = []
        # Are we starting a new dimension ?
        if not index[-1]:
            for i in range(len(index)-1,0,-1):
                if index[i]: break
                dims.insert(0,i-1)
        dims.append(len(dst.shape)-1)
        for dim in dims:
            i = index[dim]

            if toric:
                z = (indices[dim][dim] - src.shape[dim]//2 +(kernel.shape[dim]+1)%2 + src_indices[dim][i]) % src.shape[dim]
            else:
                z = (indices[dim][dim] - src.shape[dim]//2 +(kernel.shape[dim]+1)%2 + src_indices[dim][i])

            # if toric:
            #     z = (indices[dim][dim] - src.shape[dim]/2.0 -(kernel.shape[dim]+1)%2 + src_indices[dim][i]) % src.shape[dim]
            # else:
            #     z = (indices[dim][dim] - src.shape[dim]/2.0 -(kernel.shape[dim]+1)%2+ src_indices[dim][i])

            n = np.where((z >= 0)*(z < src.shape[dim]))[0]
            if not dim:
                nd[dim] = n.copy()
            else:
                nd[dim] = nd[dim-1][n]
            indices[dim+1] = np.take(indices[dim], n, 1)
            indices[dim+1][dim] = z[n]
        dim = len(dst.shape)-1
        z = indices[dim+1]
        R.extend( [dst_index,]*len(z[0]) )
        C.extend( (z*to_flat_index).sum(0).tolist() )
        D.extend( data[nd[-1]].tolist() )
        dst_index += 1

    return sp.coo_matrix( (D,(R,C)), (dst.size,src.size))

    #Z = np.zeros((dst.size,src.size))
    #Z[R,C] = D
    #return Z

    # #nz = kernel.nonzero()
    # nz = (1 - np.isnan(kernel)).nonzero()
    # data = kernel[nz].flatten()
    # indices = [0,]*(len(kernel.shape)+1)
    # indices[0] = np.array(nz)
    # indices[0] += np.atleast_2d((np.array(src.shape)//2 - np.array(kernel.shape)//2)).T
    # to_flat_index = np.ones((len(src.shape),1), dtype=int)
    # to_flat_index[:-1] = src.shape[:-1]
    # R, C, D = [], [], []
    # dst_index = 0
    # src_indices = []
    # for i in range(len(src.shape)):
    #     z = np.rint((np.linspace(0,1,dst.shape[i])*(src.shape[i]-1))).astype(int)
    #     src_indices.append(z)
    # for index in np.ndindex(dst.shape):
    #     dims = []
    #     if index[-1] == 0:
    #         for i in range(len(index)-1,0,-1):
    #             if index[i]: break
    #             dims.insert(0,i-1)
    #     dims.append(len(dst.shape)-1)
    #     for dim in dims:
    #         i = index[dim]
    #         if toric:
    #             z = (indices[dim][dim] - src.shape[dim]//2 + src_indices[dim][i]) % src.shape[dim]
    #         else:
    #             z = (indices[dim][dim] - src.shape[dim]//2 + src_indices[dim][i])
    #         n = np.where((z >= 0)*(z < src.shape[dim]))[0]
    #         indices[dim+1] = np.take(indices[dim], n, 1)
    #         indices[dim+1][dim] = z[n]
    #     dim = len(dst.shape)-1
    #     z = indices[dim+1]
    #     R.extend( [dst_index,]*len(z[0]) )
    #     C.extend( (z*to_flat_index).sum(0).tolist() )
    #     D.extend( data[n].tolist() )
    #     dst_index += 1
#    return sp.coo_matrix( (D,(R,C)), (dst.size,src.size))



def gaussian(shape=(25,25), width=0.5, center=0.0):
    """ Generate a gaussian of the form g(x) = height*exp(-(x-center)**2/width**2).

    **Parameters**

        shape: tuple of integers
           Shape of the output array

        width: float or tuple of float
           Width of gaussian

        center: float or tuple of float
           Center of gaussian

    **Returns**

       a numpy array of specified shape containing a gaussian
    """
    if type(shape) in [float,int]:
        shape = (shape,)
    if type(width) in [float,int]:
        width = (width,)*len(shape)
    if type(center) in [float,int]:
        center = (center,)*len(shape)
    grid=[]
    for size in shape:
        grid.append (slice(0,size))
    C = np.mgrid[tuple(grid)]
    R = np.zeros(shape)
    for i,size in enumerate(shape):
        if shape[i] > 1:
            R += (((C[i]/float(size-1))*2 - 1 - center[i])/width[i])**2
    return np.exp(-R/2)

def empty(shape, dtype=float):
    """
    Return a new group of given shape and type, without initialising entries.


    :param tuple shape:
        Shape of the new group, e.g., ``(2, 3)`` or ``2``.
    :param dtype:
        The desired data-type for the group, e.g., `np.int8`.  Default is
        `np.float64`.
    :return:
        Group with the given shape and dtype filled with zeros.

    **Notes**

    `empty`, unlike `zeros`, does not set the group values to zero, and may
    therefore be marginally faster.  On the other hand, it requires the user
    to manually set all the values in the group, and should be used with
    caution.

    **Examples**

    >>> Group.empty((2,2))
    Group([[6.94248367807e-310, 1.34841898023e-316],
           [1.34841977073e-316, 0.0]],
          dtype=[('f0', '<f8')])

    **See also**

    * :meth:`dana.zeros` : Return a new group setting values to zero.
    * :meth:`dana.ones` : Return a new group setting values to one.
    * :meth:`dana.zeros_like` : Return a group of zeros with shape and type of input.
    * :meth:`dana.ones_like` : Return a group of ones with shape and type of input.
    * :meth:`dana.empty_like` : Return a empty group with shape and type of input.
    """
    return Group(shape=shape, dtype=dtype, fill=None)

def zeros(shape, dtype=float):
    """
    Return a new group of given shape and type, filled with zeros.

    :param tuple shape:
        Shape of the new group, e.g., ``(2, 3)`` or ``2``.
    :param dtype:
        The desired data-type for the group, e.g., `np.int8`.  Default is
        `np.float64`.
    :return:
        Group with the given shape and dtype filled with zeros.

    **Examples**

    >>> dana.zeros((2,2))
    Group([[0.0, 0.0],
           [0.0, 0.0]],
          dtype=[('f0', '<f8')])
    >>> dana.zeros((2,2), dtype=int)
    Group([[0, 0],
           [0, 0]],
          dtype=[('f0', '<f8')])

    **See also**

    * :meth:`dana.ones` : Return a new group setting values to one.
    * :meth:`dana.empty` : Return a new uninitialized group.
    * :meth:`dana.zeros_like` : Return an group of zeros with shape and type of input.
    * :meth:`dana.ones_like` : Return an group of ones with shape and type of input.
    * :meth:`dana.empty_like` : Return an empty group with shape and type of input.
    """
    return Group(shape=shape, dtype=dtype, fill=0)

def ones(shape, dtype=float):
    """
    Return a new group of given shape and type, filled with ones.

    :param tuple shape:
        Shape of the new group, e.g., ``(2, 3)`` or ``2``.
    :param dtype:
        The desired data-type for the group, e.g., `np.int8`.  Default is
        `np.float64`.
    :return:
        Group with the given shape and dtype filled with zeros.

    **Examples**

    >>> dana.ones((2,2))
    Group([[1.0, 1.0],
           [1.0, 1.0]],
          dtype=[('f0', '<f8')])
    >>> dana.ones((2,2), dtype=int)
    Group([[1, 1],
           [1, 1]],
          dtype=[('f0', '<f8')])

    **See also**

    * :meth:`dana.zeros` : Return a new group setting values to zero.
    * :meth:`dana.empty` : Return a new uninitialized group.
    * :meth:`dana.zeros_like` : Return an group of zeros with shape and type of input.
    * :meth:`dana.ones_like` : Return an group of ones with shape and type of input.
    * :meth:`dana.empty_like` : Return an empty group with shape and type of input.
    """
    return Group(shape=shape, dtype=dtype, fill=1)

def empty_like(other):
    """
    Create a new group with the same shape and type as another.

    :param array other:
        The shape and data-type of `other` defines the parameters of the
        returned group.
    :return:
        Uninitialized group with same shape and type as `other`.

    **Examples**

    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.zeros_like(x)
    array([[0, 0, 0],
           [0, 0, 0]])

    **See also**

    * :meth:`dana.zeros` : Return a new group setting values to zero.
    * :meth:`dana.ones` : Return a new group setting values to one.
    * :meth:`dana.empty` : Return a new uninitialized group.
    * :meth:`dana.ones_like` : Return a group of ones with shape and type of input.
    * :meth:`dana.zeros_like` : Return a group of zeros with shape and type of input.
    """
    return Group(shape=other.shape, dtype=other.dtype, fill=None)

def zeros_like(other):
    """
    Create a new group of zeros with the same shape and type as another.


    :param array other:
        The shape and data-type of `other` defines the parameters of the
        returned group.
    :return:
        Group of zeros with same shape and type as `other`.

    **Examples**

    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.zeros_like(x)
    array([[0, 0, 0],
           [0, 0, 0]])

    **See also**

    * :meth:`dana.zeros` : Return a new group setting values to zero.
    * :meth:`dana.ones` : Return a new group setting values to one.
    * :meth:`dana.empty` : Return a new uninitialized group.
    * :meth:`dana.empty_like` : Return an uninitialized group shape and type of input.
    * :meth:`dana.ones_like` : Return a group of ones with shape and type of input.
    """
    return Group(shape=other.shape, dtype=other.dtype, fill=0)

def ones_like(other):
    """
    Returns a group of ones with the same shape and type as a given array.

    :param array other:
        The shape and data-type of `other` defines the parameters of the
        returned group.
    :return:
        Group of ones with same shape and type as `other`.

    **Examples**

    >>> x = np.arange(6)
    >>> x = x.reshape((2, 3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> zeros_like(x)
    group([[0, 0, 0],
           [0, 0, 0]])

    **See also**

    * :meth:`dana.zeros` : Return a new group setting values to zero.
    * :meth:`dana.ones` : Return a new group setting values to one.
    * :meth:`dana.empty` : Return a new uninitialized group.
    * :meth:`dana.empty_like` : Return an empty group with shape and type of input.
    * :meth:`dana.zeros_like` : Return a group of zeros with shape and type of input.
    """
    return Group(shape=other, dtype=other.dtype, fill=1)
