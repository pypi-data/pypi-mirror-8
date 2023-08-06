#
#   Copyright (c) 2014, Scott J Maddox
#
#   This file is part of SimpleQW.
#
#   SimpleQW is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   SimpleQW is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public
#   License along with SimpleQW.  If not, see
#   <http://www.gnu.org/licenses/>.
#
#######################################################################

from libc.math cimport sqrt, asin

cdef double pi = 3.14159265359
# h = 6.62606957e-34  # J * s
cdef double hbar = 1.05457173e-34  # J * s
cdef double eV = 1.60217657e-19  # J
cdef double m_e = 9.10938215e-31  # kg
cdef double nm = 1e-9  # m
cdef double _P_prefactor = (sqrt(2. * m_e * eV) / hbar) * (nm / 2.)
cdef double _E_units = hbar ** 2 / (m_e * nm ** 2) / eV

cpdef int num_states_scaled(double P):
    '''
    Returns the number of bound states in a finite-potential quantum well
    with the given well-strength parameter, `P`.

    References
    ----------
        D.L. Aronstein and C.R. Stroud, Jr., Am. J. Phys. 68, 943 (2000).
    '''
    return int(P / (pi / 2.)) + 1


cpdef double energy_scaled(double P, int n=1, double atol=1e-6):
    '''
    Returns the nth bound-state energy [hbar ** 2. / (m * L ** 2.))] for a
    finite-potential quantum well with the given well-strength parameter, `P`.

    Parameters
    ----------
    P : double
        the well-strength parameter, P = sqrt(2 * m * V) / hbar * L / 2
    n : int
        the quantum number of the desired state. 1 <= n <= num_states(P)
    atol : double
        the absolute tolerance of the resulting energy

    Returns
    -------
    energy : double
        the bound-state energy [hbar ** 2. / (m * L ** 2.))]

    References
    ----------
        D.L. Aronstein and C.R. Stroud, Jr., Am. J. Phys. 68, 943 (2000).
    '''
    cdef double pi_2, r, eta, w, r2, sqrt_1mr2, denom, t1, next_r, next_eta
    cdef double alpha, E
    assert n > 0 and n <= num_states_scaled(P)
    pi_2 = pi / 2.
    r = (1 / (P + pi_2)) * (n * pi_2)
    eta = n * pi_2 - asin(r) - r * P
    w = 1  # relaxation parameter (for succesive relaxation)
    while True:
        if abs(eta) < atol:
            break
        r2 = r ** 2.
        sqrt_1mr2 = sqrt(1. - r2)
        denom = (1. + P * sqrt_1mr2)
        t1 = P * sqrt_1mr2 / denom * eta
#         t2 = -r * P / (2 * (1. + P * sqrt_1mr2) ** 3) * eta ** 2
        while True:
            next_r = (1 - w) * r + w * (r + t1)
#             next_r = (1 - w) * r + w * (r + t1 + t2)
            next_eta = n * pi_2 - asin(next_r) - next_r * P
            # decrease w until eta is converging
            if abs(next_eta / eta) < 1:
                r = next_r
                eta = next_eta
                break
            else:
                w *= 0.5

    alpha = P * r
    E = 2. * (alpha) ** 2.  # hbar ** 2. / (m * L ** 2.))
    return E

cpdef double energy(double L, double m, double U, int n=1, double atol=1e-6):
    '''
    Returns the nth bound-state energy [eV] for a finite-potential quantum
    well with the given well-strength parameter, `P`.

    If U <= 0, returns 0.

    Parameters
    ----------
    L : double
        thickness of the well [nm]
    m : double
        effective mass in the well [electron mass]
    U : double
        the potential [eV]
    n : int
        the quantum number of the desired state
    atol : double
        the absolute tolerance of the resulting energy

    Returns
    -------
    energy : double
        the bound-state energy [eV]

    References
    ----------
        D.L. Aronstein and C.R. Stroud, Jr., Am. J. Phys. 68, 943 (2000).
    '''
    
    if U <= 0.:
        return 0.
    cdef double P = _P_prefactor * L * sqrt(m * U)
    return energy_scaled(P, n, atol) * _E_units / (m * L ** 2.)
