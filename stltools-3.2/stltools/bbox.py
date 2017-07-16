# file: bbox.py
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
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
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

"""Operations on two or three dimensional bounding boxes."""

import numpy as np

__version__ = '$Revision: 3.2 $'[11:-2]


def makebb(pnts):
    """Find the bound for a list of points

    :pnts: numpy array, shape (N,2) or (N,3)
    :returns: an array [minx, maxx, miny, maxy[, minz, maxz]
    """
    if len(pnts.shape) != 2:
        raise ValueError('invalid shape')
    dim = pnts.shape[-1]
    out = []
    for n in range(dim):
        out.append(np.min(pnts.T[n]))
        out.append(np.max(pnts.T[n]))
    return np.array(out)


def inside(bb, v):
    """Test if a point is inside a bounding box.

    :bb: bounding box numpy array
    :v: point array
    :returns: True if v is inside the bounding box, false otherwise.
    :raises: ValueError if the number of dimensions of the point and bounding
    box don't match.
    """
    if len(bb.shape) != 1:
        raise ValueError('invalid shape')
    if bb.shape[0] != 2*v.shape[0]:
        raise ValueError('incompatible shape')
    mi, ma = bb.reshape((-1, 2)).T
    return np.all(v >= mi) and np.all(v <= ma)
