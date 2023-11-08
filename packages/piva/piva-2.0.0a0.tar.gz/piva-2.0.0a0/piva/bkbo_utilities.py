import math
from itertools import groupby

# from scipy import optimize as opt
import matplotlib as mpl
import numpy as np
from numba import njit, prange
# from numba_progress import ProgressBar
import pandas as pd
import scipy.signal as sig
from matplotlib import pyplot as plt
from matplotlib import colors, patches, interactive
from numpy.linalg import norm   # for shriley bckgrd
from scipy.special import voigt_profile
from scipy import ndimage
from scipy.optimize import curve_fit, minimize, fsolve
from scipy.signal import convolve2d
from scipy.optimize import OptimizeWarning
from scipy.fft import fft, ifft, fft2, ifft2, fftshift, ifftshift
# from mp_api.client import MPRester

import piva.data_loaders as dl
import piva.constants as const


@njit(parallel=True)
def get_cut_along_angle(alpha, data, xx, yy, N, z, xbin, ybin, nb=10, rl=3):

    kx, ky = np.abs(z) * np.cos(alpha), np.abs(z) * np.sin(alpha)
    cut = np.zeros((N, data.shape[2]))
    for idx in range(kx.size):
        kx_idx, ky_idx = np.argmin(np.abs(xx - kx[idx])), \
                         np.argmin(np.abs(yy - ky[idx]))
        if xbin == 0:
            cut[idx, :] = np.sum(data[kx_idx, (ky_idx - ybin):(ky_idx + ybin), :], axis=0)
        elif ybin == 0:
            cut[idx, :] = np.sum(data[(kx_idx - xbin):(kx_idx + xbin), ky_idx, :], axis=0)
        else:
            cut[idx, :] = np.sum(np.sum(data[(kx_idx - xbin):(kx_idx + xbin),
                                       (ky_idx - ybin):(ky_idx + ybin), :], axis=1), axis=0)

    return cut
    # print(xbin, ybin, cut.shape, cut.max())
    # tmp['cut'] = wp.smooth_2d(cut, n_box=15, recursion_level=3)

