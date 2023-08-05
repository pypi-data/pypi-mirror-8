# -*- coding: utf-8 -*-

# Copyright (c) 2012, Sergio Callegari
# All rights reserved.

# This file is part of PyDSM.

# PyDSM is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyDSM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyDSM.  If not, see <http://www.gnu.org/licenses/>.

"""
Computation of the noise power gain through the NTF and the output filter
=========================================================================
"""

import numpy as np
import scipy as sp
__import__("scipy.signal")
from ...ir import impulse_response
from ...delsig import evalTF
from ..weighting import quantization_weighted_noise_gain
from ...errors import PyDsmError

__all__ = ["quantization_noise_gain", "quantization_noise_gain_by_conv"]

def quantization_noise_gain(NTF, H, H_type='zpk'):
    r"""
    Computes the quantization noise power gain

    Parameters
    ----------
    NTF : tuple
        NTF definition in zpk or nd form
    H : tuple or callable or array_like
        output filter definition in zpk or ba form if H_type='zpk' or 'ba'
        (in this case, H is a tuple with 3 or 2 entries);
        output filter magnitude response if H_type='mag' (in this case, H is
        a callable with argument f in [0,1/2]);
        output filter impulse response if H_type='imp' (in this case, H is an
        array)
    H_type : str
        type of specification for parameter H. One of: 'zpk', 'ba', 'mag' or
        'imp'

    Returns
    -------
    a : real
        noise power gain

    Notes
    -----
    In the default case the computation is practiced as

    .. math::
        2\int_{f=0}^{\frac{1}{2}}
        \left|H\left(\mathrm{e}^{\mathrm{i} 2\pi f}\right)\right|^2
        \left|\mathit{NTF}
        \left(\mathrm{e}^{\mathrm{i} 2\pi f}\right)\right|^2 df
    """
    if H_type=='zpk' or H_type=='ba':
        w = lambda f: np.abs(evalTF(H,np.exp(2j*np.pi*f)))**2
    elif H_type=='imp':
        w = lambda f: np.abs(evalTF((H,1),np.exp(2j*np.pi*f)))**2
    elif H_type=='mag':
        w = lambda f: H(f)**2
    else:
        raise PyDsmError("Incorrect filter type specification")
    return quantization_weighted_noise_gain(NTF, w)


def quantization_noise_gain_by_conv(NTF, H, H_type='zpk', db=80):
    """
    Computes the quantization noise power gain, based on a convolution

    Parameters
    ----------
    NTF : tuple
        NTF definition in zpk or nd form
    H : tuple or array_like
        output filter definition in zpk or nd form if H_type='zpk' or 'ba'
        (in this case, H is a tuple with 3 or 2 entries);
        output filter impulse response if H_type='imp' (in this case, H is an
        array)
    H_type : str
        type of specification for parameter H. One of: 'zpk', 'ba', or
        'imp'
    db : real
        a precision hint for the computation of impulse responses

    Returns
    -------
    a : real
        noise power gain

    Notes
    -----
    The computation is practiced as the sum of the squared entries
    in the impulse response of the cascaded filter NTF*H
    """
    h1_ir=impulse_response(NTF, db=db)
    if H_type=='zpk' or H_type=='ba':
        h2_ir=impulse_response(H, db=db)
    elif H_type=='imp':
        h2_ir = H
    else:
        raise PyDsmError("Incorrect filter type specification")
    conv = sp.signal.convolve(h1_ir, h2_ir)
    return np.sum(conv**2)
