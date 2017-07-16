# file: vecops.py
# vim:fileencoding=utf-8
#
# Copyright © 2013,2014 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2013-06-10 22:41:00 +0200
# $Date: 2014-06-15 17:12:40 +0200 $
# $Revision: 3.2 $
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Operations of two or three dimensional vectors."""

import numpy as np
import math as m

__version__ = '$Revision: 3.2 $'[11:-2]


def length(v):
    """Returns the length of a vector.

    :v: numpy vector
    """
    return m.sqrt(np.sum(v*v))


def normalize(v):
    """Returns the vector scaled to lenth 1.

    :v: numpy vector
    """
    l = length(v)
    return v/l


def normal(a, b, c):
    """Calculate the normal vector for the triangle defined by a, b and c.

    :a, b, c: numpy array of shape (3,)
    :returns: a vector normal to the plane formed by a, b and c.
    """
    u = b - a
    v = c - b
    n = np.cross(u, v)
    l = length(n)
    if l:
        return n/l
    return n


def indexate(points):
    """Convert a numpy array of points into a list of indices and an array of
    unique points.

    :points: a numpy array of shape (N, 3)
    :returns: a tuple of indices and an array of unique points
    """
    pd = {}
    indices = [pd.setdefault(tuple(p), len(pd)) for p in points]
    pt = sorted([(v, k) for k, v in pd.iteritems()], key=lambda x: x[0])
    unique = np.array([i[1] for i in pt])
    return np.array(indices, np.uint16), unique


def to4(pnts):
    """Converts 3D coordinates to homogeneous coordinates.

    :pnts: a numpy array of shape (N,3)
    :returns: a numpy array of shape (N,4)
    """
    if len(pnts.shape) != 2 or pnts.shape[1] != 3:
        raise ValueError('invalid shape')
    return np.vstack((pnts.T, np.ones(pnts.shape[0]))).T


def to3(pnts):
    """Converts homogeneous coordinates to plain 3D coordinates.
    It scales the x, y and z values by the w value.

    :pnts: a numpy array of shape (N,4)
    :returns: a numpy array of shape (N,3)
    """
    if len(pnts.shape) != 2 or pnts.shape[1] != 4:
        raise ValueError('invalid shape')
    d = pnts[:, 3]
    div = np.vstack((d, d, d)).T
    return pnts[:, 0:3]/div


def xform(mat, pnts):
    """Apply a transformation matrix to a numpy array of points.

    :mat: 3x3 or 4x4 numpy array
    :pnts: (N,3) or (N,4) numpy array
    :returns: transformed array
    """
    if len(pnts.shape) != 2 and pnts.shape[1] not in (3, 4):
        raise ValueError('wrong shape of pnts')
    conv = False
    if mat.shape == (3, 3):
        if pnts.shape[1] == 4:
            raise ValueError('homogeneous coordinates with 3x3 matrix')
    elif mat.shape == (4, 4):
        if pnts.shape[1] == 3:
            pnts = to4(pnts)
            conv = True
    else:
        raise ValueError('wrong shape of matrix')
    rv = np.array([np.dot(mat, v) for v in pnts])
    if conv:
        return to3(rv)
    return rv
