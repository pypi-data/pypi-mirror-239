from pyccel.decorators import pure

from numpy import sin, cos


def _docstring():
    '''MODULE DOCSTRING for :ref:`kinetic_moments`.

    The module contains pyccelized functions that can be used to specify moments of background distribution functions f0.

    The main method is :math:`kinetic_moments.moments` at the end of the file, which calls the functions defined before.

    New functions must be added at the top of the file, right after the docstring. 
    In the "Note" of the new function you must state a **moment specifier**; this is an integer that identifies the function in 
    the if-clause of :math:`kinetic_moments.moments`.'''

    print('This is just the docstring function.')


@pure
def modes_sin_cos(x: 'float', y: 'float', z: 'float',
                  n_modes: 'int',
                  kxs: 'float[:]', kys: 'float[:]', kzs: 'float[:]',
                  amps_sin: 'float[:]', amps_cos: 'float[:]') -> float:
    r'''
    Point-wise evaluation of  

    .. math::

        u(x, y, z) = \sum_{i=0}^N \left[ A_i\sin(k_{x,i}\,x + k_{y,i}\,y + k_{z,i}\,z) + B_i\cos(k_{x,i}\,x + k_{y,i}\,y + k_{z,i}\,z) \right]\,.

    Parameters
    ----------
        x,y,z : float
            Evaluation point.

        n_modes: int
            Number of modes, >0. 

        kxs : array[float]
            Mode numbers in x-direction, kx = o*2*pi/Lx.

        kys : array[float]
            Mode numbers in y-direction, ky = m*2*pi/Ly.

        kzs : array[float]
            Mode numbers in z-direction, kz = n*2*pi/Lz.

        amps_sin : array[float]
            Amplitude of sine function for each mode k = (kx, ky, kz).

        amps_cos : array[float]
            Amplitude of cosine function for each mode k = (kx, ky, kz).

    Notes
    -----
        Specifier: 1
    '''

    value = 0.
    for k in range(n_modes):
        value += amps_sin[k]*sin(kxs[k]*x + kys[k]*y + kzs[k]*z) + \
            amps_cos[k]*cos(kxs[k]*x + kys[k]*y + kzs[k]*z)

    return value


def moments(eta: 'float[:]', moms_spec: 'int[:]', params: 'float[:]'):
    r"""
    Point-wise evaluation at logical (eta1, eta2, eta3) of the moments density, mean velocity and thermal velocity:

    .. math::

        n_0(\mathbf x) &= \int f_0(\mathbf x, \mathbf v)\,\textnormal d \mathbf v

        \mathbf u_0(\mathbf x) &= \frac{1}{n_0(\mathbf x)} \int \mathbf v\, f_0(\mathbf x, \mathbf v)\,\textnormal d \mathbf v

        v_{\textnormal{th},0,i}(\mathbf x) &= \sqrt{\frac{1}{n_0(\mathbf x)} \int \mathbf |v_i - u_{0,i}|^2\, f_0(\mathbf x, \mathbf v)\,\textnormal d \mathbf v }

    Parameters
    ----------
        eta : array[float]
            Position at which to evaluate the moments.

        moms_spec : array[int]
            Specifier for the seven moments n0, u01, u02, u03, vth01, vth02, vth03 (in this order).
            Is 0 for constant moment, for more see Notes.

        params : array[float]
            Parameters needed to specify the moments; the order is specified in :ref:`kinetic_moments` in the function's docstrings.

    Returns
    -------
        The function values at (eta1, eta2, eta3).

    Notes
    -----
        See :ref:`kinetic_moments` for available moment functions.
    """

    ind = 0  # helps you count through params

    # density
    if moms_spec[0] == 0:  # constant value
        n0 = params[ind]
        ind += 1
    elif moms_spec[0] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        n0 = modes_sin_cos(eta[0], eta[1], eta[2], n_modes,
                           kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[0]', moms_spec[0])

    # x-momentum
    if moms_spec[1] == 0:  # constant value
        u01 = params[ind]
        ind += 1
    elif moms_spec[1] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        u01 = modes_sin_cos(eta[0], eta[1], eta[2],
                            n_modes, kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[1]', moms_spec[1])

    # y-momentum
    if moms_spec[2] == 0:  # constant value
        u02 = params[ind]
        ind += 1
    elif moms_spec[2] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        u02 = modes_sin_cos(eta[0], eta[1], eta[2],
                            n_modes, kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[2]', moms_spec[2])

    # z-momentum
    if moms_spec[3] == 0:  # constant value
        u03 = params[ind]
        ind += 1
    elif moms_spec[3] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        u03 = modes_sin_cos(eta[0], eta[1], eta[2],
                            n_modes, kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[3]', moms_spec[3])

    # x-thermal velocity
    if moms_spec[4] == 0:  # constant value
        vth01 = params[ind]
        ind += 1
    elif moms_spec[4] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        vth01 = modes_sin_cos(eta[0], eta[1], eta[2],
                              n_modes, kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[4]', moms_spec[4])

    # y-thermal velocity
    if moms_spec[5] == 0:  # constant value
        vth02 = params[ind]
        ind += 1
    elif moms_spec[5] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        vth02 = modes_sin_cos(eta[0], eta[1], eta[2],
                              n_modes, kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[5]', moms_spec[5])

    # z-thermal velocity
    if moms_spec[6] == 0:  # constant value
        vth03 = params[ind]
        ind += 1
    elif moms_spec[6] == 1:  # modes_sin_cos
        n_modes = int(params[ind])
        ind += 1
        kxs = params[ind: ind + n_modes]
        ind += n_modes
        kys = params[ind: ind + n_modes]
        ind += n_modes
        kzs = params[ind: ind + n_modes]
        ind += n_modes
        amps_sin = params[ind: ind + n_modes]
        ind += n_modes
        amps_cos = params[ind: ind + n_modes]
        ind += n_modes
        vth03 = modes_sin_cos(eta[0], eta[1], eta[2],
                              n_modes, kxs, kys, kzs, amps_sin, amps_cos)
    else:
        print('Invalid moms_spec[6]', moms_spec[6])

    return n0, u01, u02, u03, vth01, vth02, vth03


def array_moments(eta: 'float[:,:]',
                  moms_spec: 'int[:]', params: 'float[:]',
                  n0: 'float[:]',
                  u01: 'float[:]', u02: 'float[:]', u03: 'float[:]',
                  vth01: 'float[:]', vth02: 'float[:]', vth03: 'float[:]'):
    r"""
    Point-wise evaluation at every (ip) logical particle positions (eta1, eta2, eta3) of the moments density, mean velocity and thermal velocity:

    Parameters
    ----------
        eta : rank2 array[float]
            Array of every particle positions at which to evaluate the moments.

        moms_spec : array[int]
            Specifier for the seven moments n0, u01, u02, u03, vth01, vth02, vth03 (in this order).

        params : array[float]
            Parameters needed to specify the moments; the order is specified in :ref:`kinetic_moments` in the function's docstrings.

        n0    : array[float]
            Array of density moment at ip.

        u01   : array[float]
            Array of 1st comp of mean velocity at ip.

        u02   : array[float]
            Array of 2nd comp of mean velocity at ip.

        u03   : array[float]
            Array of 3rd comp of mean velocity at ip.

        vth01 : array[float]
            Array of 1st comp of thermal velocity at ip.

        vth02 : array[float]
            Array of 2nd comp of thermal velocity at ip.

        vth03 : array[float]
            Array of 3rd comp of thermal velocity at ip.

    Notes
    -----
        See :ref:`kinetic_moments` for available moment functions.
    """

    for ip in range(len(eta[:, 0])):
        n0[ip], u01[ip], u02[ip], u03[ip], vth01[ip], vth02[ip], vth03[ip] = moments(
            eta[ip, :], moms_spec, params)
