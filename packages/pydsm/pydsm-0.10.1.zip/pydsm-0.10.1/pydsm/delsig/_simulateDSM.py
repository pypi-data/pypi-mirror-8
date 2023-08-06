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
Entry point for DELSIG-like Delta-Sigma modulator simulator
===========================================================
"""

from ._simulateDSM_scipy import simulateDSM as simulateDSM_slow
try:
    from ._simulateDSM_cblas import simulateDSM as simulateDSM_cblas
except:
    pass
from ._simulateDSM_scipy_blas import simulateDSM as simulateDSM_scipy_blas

__all__ = ["use_fast_simulator", "simulateDSM"]

try:
    simulateDSM_fast = simulateDSM_cblas
except:
    simulateDSM_fast = simulateDSM_scipy_blas

use_fast_simulator = True


def simulateDSM(u, arg2, nlev=2, x0=0,
                store_xn=False, store_xmax=False, store_y=False):
    """
    Computes the output of a general delta-sigma modulator.

    Parameters
    ----------
    u : array_like or matrix_like
        modulator input. Multiple inputs are allowed. In this case,
        u is a matrix with as many rows as the desired inputs
    arg2 : tuple
        modulator structure in ABDC matrix form or modulator NTF
        as zpk tuple. In the latter case, the modulator STF is assumed
        to be unitary.
    nlev : int or array of ints, optional
        number of levels in quantizer. Multiple quantizers can be
        specified by making nlev a vector. Defaults to 2.
    x0 : array_like of reals or 0
        modulator intitial state vector. Assigning it to 0 is a shorthand
        for an appropriate length zero vector. Defaults to 0.
    store_xn : bool, optional
        switch controlling the storage of state evolution.
        See description of return values. Defaults to False.
    store_xmax : bool, optional
        switch controlling the storage of maxima in state variables.
        See description of return values. Defaults to False.
    store_y : bool, optional
        switch controlling the storage of input quantizer values.
        See description of return values. Defaults to False.

    Returns
    -------
    v : ndarray
        samples at the output of the modulator, one per input sample.
        If there are multiple quantizers, then v is a matrix, with as many
        columns as the number of samples and as many rows as the number of
        quantizers.
    xn : ndarray
        internal state of the modulator. If store_xn is set to True, then
        it includes a state snapshot per input sample. In this case, xn
        is a matrix, with as many columns as the number of samples and as
        many rows as the number of state variables. If store_xn is False,
        then xn is a vector containing a snapshot of the last state.
    xmax : ndarray
        maximum absolute value reached by the state variables.
        If store_xmax is set to True, then xmax is a vector with as many
        entries as the number of state variables. Otherwise it is null.
        y -> samples at the quantizer input(s), one per input sample.
    y : ndarray
        samples at the quantizer input(s), one per input sample.
        If store_y is set to True, then y records the quantizer(s)
        input(s). If there are multiple quantizers, then y is a matrix,
        with as many columns as the number of samples and as many rows as
        the number of quantizers. If store_y is False, then y is null.

    Raises
    ------
    PyDsmError
        'Incorrect modulator specification', if the modulator specification
        is inconsistent.

    Warns
    -----
    PyDsmWarning
        'Running the slow version of simulateDSM.', if the simulator being
        used is the slow one, coded in pure Python.

    Notes
    -----
    The quantizer is ideal, producing integer outputs centered about zero.
    Quantizers with an even number of levels are of the mid-rise type and
    produce outputs which are odd integers. Quantizers with an odd number of
    levels are of the mid-tread type and produce outputs which are even
    integers.

    The modulator structure being simulated is a block diagonal one, as
    returned by the zpk2ss function.

    Setting store_xn, store_xmax and store_y to False speeds up the operation.

    There are actually two simulators, sharing this function as a front end.
    One of them is coded in pure python and quite slow. The other one is
    coded in C (actually in Cython), and directly accesses low level cblas
    functions. The codebase to be used is controlled by the module switch
    `use_fast_simulator`.
    """

    if use_fast_simulator:
        return simulateDSM_fast(u, arg2, nlev, x0,
                                store_xn, store_xmax, store_y)
    else:
        return simulateDSM_slow(u, arg2, nlev, x0,
                                store_xn, store_xmax, store_y)
