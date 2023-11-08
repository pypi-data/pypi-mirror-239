# functions and other shit for data processing specific for TaSe{2-x}S{x} and VxTaS2 systems

import numpy as np
import piva.constants as const

# hopping parameters for both bands in meV, taken from li2018_sm.pdf
# lattice consts in A
a_TaSe2 = 3.4552            # doi: 10.1103/PhysRevB.59.6063
a_TaS2 = 3.314              # doi: 10.1107/S0108270190000014
a_TaS2_1T = 3.36
c_TaS2_2H = 12.07
c_TaS2_1T = 5.85


def get_lattice_const(x=0, rec=1):
    if 0 < x <= 2:
        return (((2 - x) * a_TaSe2 + x * a_TaS2) / 2) * np.sqrt(rec)
    else:
        return x * np.sqrt(rec)


def get_vts_lc(x=0.1, a=True):
    k = x / 0.15
    if a:
        return (1 - k) * a_TaS2 + k * a_TaS2_1T
    else:
        return (1 - k) * c_TaS2_2H + k * c_TaS2_1T


def get_initial_t(model='li2018'):
    if model == 'li2018':
        t_barrel = np.array([-45.1, 157.8, 203.2, 25.7, 0.02, 0.48])
        t_dogbone = np.array([501.3, -15.9, 557.1, -72.0, -13.9, 12.2])
    elif model == 'rossnagel2005':
        t_barrel = np.array([-0.0373, 0.276, 0.2868, 0.007]) * 1000
        t_dogbone = np.array([0.4108, -0.0726, 0.4534, -0.12]) * 1000
    elif model == 'inosov2008':
        t_barrel = np.array([-0.064, 0.167, 0.211, 0.005, 0.003]) * 1000
        t_dogbone = np.array([0.369, 0.074, 0.425, -0.049, 0.018]) * 1000
    elif model == 'smith1985':
        Ef = 0.3753
        dz2 = 0.4698
        dxy = 0.4653
        orb = np.array([dz2, dxy])
        orb = const.convert_eV_Ry(orb)

        sigma = -0.05483
        pi = 0.01769
        delta = 0.00802
        t0 = 0.5 * (sigma + 3 * delta)
        t11, t12 = 0.25 * (3 * sigma + 12 * pi + delta), 0.5 * (3 * sigma + delta)
        t21, t22 = 0.25 * (9 * sigma + 4 * pi + 3 * delta), 2 * pi
        t31, t32 = 3 * pi + delta, 2 * delta
        t41, t42 = pi + 3 * delta, 2 * pi
        t5 = 0.5 * np.sqrt(3) * (sigma - delta)
        t6 = 1.5 * (sigma - delta)
        t7 = 0.25 * np.sqrt(3) * (3 * sigma - 4 * pi + delta)
        t8 = -np.sqrt(3) * (pi - delta)
        t = np.array([t0, t11, t12, t21, t22, t31, t32, t41, t42, t5, t6, t7, t8])
        t = const.convert_eV_Ry(t)
        return orb, t
    else:
        print('Wrong model given.')
        return
    return t_dogbone, t_barrel


def coords_trans(kx, ky, x=2, rec=1, flip=False):
    # for TaSe2 kx and ky flipped comparing to li2018_sm.pdf
    a = get_lattice_const(x=x, rec=rec)
    if flip:
        Xi = np.sqrt(3) * 0.5 * kx * a
        Eta = 0.5 * ky * a
    else:
        Xi = 0.5 * kx * a
        Eta = np.sqrt(3) * 0.5 * ky * a
    return np.array(Xi), np.array(Eta)


def TB_Ek(kx, ky, *t, x=2, flip=False, model='li2018'):

    kxx, kyy = coords_trans(kx, ky, x=x, flip=flip)
    E_k = np.zeros((kxx.size, kyy.size))

    if model == 'li2018':
        Xi = kxx
        Eta = kyy
        for i, xi in enumerate(Xi):
            for j, eta in enumerate(Eta):
                E_k[i][j] = t[0] + t[1] * (2 * np.cos(xi) * np.cos(eta) + np.cos(2 * xi)) + \
                            t[2] * (2 * np.cos(3 * xi) * np.cos(eta) + np.cos(2 * eta)) + \
                            t[3] * (2 * np.cos(2 * xi) * np.cos(2 * eta) + np.cos(4 * xi)) + \
                            t[4] * (np.cos(xi) * np.cos(3 * eta) + np.cos(5 * xi) * np.cos(eta) +
                                    np.cos(4 * xi) * np.cos(2 * eta)) + \
                            t[5] * (np.cos(3 * xi) * np.cos(3 * eta) + np.cos(6 * xi))
    elif model == 'rossnagel2005':
        Xi = kxx
        Eta = kyy
        for i, xi in enumerate(Xi):
            for j, eta in enumerate(Eta):
                E_k[i][j] = t[0] + t[1] * (2 * np.cos(xi) * np.cos(eta) + np.cos(2 * xi)) + \
                            t[2] * (2 * np.cos(3 * xi) * np.cos(eta) + np.cos(2 * eta)) + \
                            t[3] * (2 * np.cos(2 * xi) * np.cos(2 * eta) + np.cos(4 * xi))
    elif model == 'inosov2008':
        if flip:
            Xi = ky * 0.5
            Eta = kx * np.sqrt(3) * 0.5
        else:
            Xi = kx * 0.5
            Eta = ky * np.sqrt(3) * 0.5
        for i, xi in enumerate(Xi):
            for j, eta in enumerate(Eta):
                E_k[i][j] = t[0] + t[1] * (2 * np.cos(xi) * np.cos(eta) + np.cos(2 * xi)) + \
                            t[2] * (2 * np.cos(3 * xi) * np.cos(eta) + np.cos(2 * eta)) + \
                            t[3] * (2 * np.cos(2 * xi) * np.cos(2 * eta) + np.cos(4 * xi)) + \
                            t[4] * (2 * np.cos(6 * xi) * np.cos(2 * eta) + np.cos(4 * xi))
                if E_k[i][j] > 50:
                    E_k[i][j] = 50

    return E_k


def TB_Ek_1T(kx, ky, orb, *t, x=3.37, rec=1, flip=False):

    kxx, kyy = coords_trans(kx, ky, x=x, flip=flip, rec=rec)
    # kxx, kyy = kx, ky
    try:
        E_k = np.zeros((kxx.size, kyy.size))
    except AttributeError:
        E_k = np.zeros(kxx.size)

    try:
        Xi = kxx
        Eta = kyy
        for i, xi in enumerate(Xi):
            for j, eta in enumerate(Eta):
                E_k[i][j] = orb[0] + t[0] * (2 * np.cos(xi) * np.cos(eta) + np.cos(2 * xi)) + \
                            orb[1] + t[1] * np.cos(xi) * np.cos(eta) + t[2] * np.cos(2 * xi) + \
                            orb[1] + t[3] * np.cos(xi) * np.cos(eta) + t[4] * np.cos(2 * xi) + \
                            t[9] * (np.cos(xi) * np.cos(eta) - np.cos(2 * xi)) + \
                            t[10] * np.sin(xi) * np.sin(eta) + \
                            t[11] * np.sin(xi) * np.sin(eta) + \
                            t[5] * np.cos(xi) * np.cos(eta) + t[6] * np.cos(2 * xi) + \
                            t[7] * np.cos(xi) * np.cos(eta) + t[8] * np.cos(2 * xi) + \
                            t[12] * np.sin(xi) * np.sin(eta)
    except TypeError:
        Xi = kxx
        eta = kyy
        for i, xi in enumerate(Xi):
            E_k[i] = t[0] + t[1] * (2 * np.cos(xi) * np.cos(eta) + np.cos(2 * xi)) + \
                        t[2] * (2 * np.cos(3 * xi) * np.cos(eta) + np.cos(2 * eta)) + \
                        t[3] * (2 * np.cos(2 * xi) * np.cos(2 * eta) + np.cos(4 * xi))

    Ef = 0.3753
    Ef = const.convert_eV_Ry(Ef)
    return E_k - Ef


def TB_Ek_fitting(K_points, *t, model='li2018'):
    Xi, Eta = K_points
    if model == 'li2018':
        E_k = t[0] + t[1] * (2 * np.cos(Xi) * np.cos(Eta) + np.cos(2 * Xi)) + \
              t[2] * (2 * np.cos(3 * Xi) * np.cos(Eta) + np.cos(2 * Eta)) + \
              t[3] * (2 * np.cos(2 * Xi) * np.cos(2 * Eta) + np.cos(4 * Xi)) + \
              t[4] * (np.cos(Xi) * np.cos(3 * Eta) + np.cos(5 * Xi) * np.cos(Eta) + np.cos(4 * Xi) * np.cos(2 * Eta)) +\
              t[5] * (np.cos(3 * Xi) * np.cos(3 * Eta) + np.cos(6 * Xi))
    elif model == 'rossnagel2005':
        E_k = t[0] + t[1] * (2 * np.cos(Xi) * np.cos(Eta) + np.cos(2 * Xi)) + \
                    t[2] * (2 * np.cos(3 * Xi) * np.cos(Eta) + np.cos(2 * Eta)) + \
                    t[3] * (2 * np.cos(2 * Xi) * np.cos(2 * Eta) + np.cos(4 * Xi))
    elif model == 'inosov2008':
        E_k = t[0] + t[1] * (2 * np.cos(Xi) * np.cos(Eta) + np.cos(2 * Xi)) + \
                    t[2] * (2 * np.cos(3 * Xi) * np.cos(Eta) + np.cos(2 * Eta)) + \
                    t[3] * (2 * np.cos(2 * Xi) * np.cos(2 * Eta) + np.cos(4 * Xi)) + \
                    t[4] * (2 * np.cos(6 * Xi) * np.cos(2 * Eta) + np.cos(4 * Xi))

    return E_k
