"""
File: psf2otf.py
Author: Nrupatunga
Email: nrupatunga.s@byjus.com
Github: https://github.com/nrupatunga
Description: Implementation of matlab's psf2otf

Notes: In order to understand psf2otf:

FFT does cyclic convolution. To understand what cyclic convolution is
please refer to the document below (also in the docs)
https://www.docdroid.net/YSKkZ5Y/fft-based-2d-cyclic-convolution-pdf#page=5
"""
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def circshift(psf: np.ndarray, shift: np.ndarray) -> np.ndarray:
    """Circular shifts

    @psf: input psf
    @shift: shifts correspoinding to each dimension
    @returns: TODO

    """
    shift = np.int32(shift)
    for i in range(shift.size):
        psf = np.roll(psf, shift[i], axis=i)

    return psf


def surf_plot(data: np.ndarray):

    x = np.linspace(0, data.shape[1], data.shape[1])
    y = np.linspace(0, data.shape[0], data.shape[0])
    x, y = np.meshgrid(x, y)
    z = np.abs(data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('surface plot')
    plt.show()


def psf2otf(psf: np.ndarray, out_size: tuple, show_plot:
            Optional[bool] = False) -> np.ndarray:
    """Implementation of matlab's psf2otf

    @psf: point spread function
    @out_size: out size
    """
    if not np.any(psf):
        print('Input psf should not contain zeros')

    psf_size = psf.shape
    assert len(psf_size) < 3, 'Number of channels is greater than 2'
    new_psf = np.zeros(out_size, dtype=np.float32)
    new_psf[:psf_size[0], :psf_size[1]] = psf[:, :]

    psf_size = np.asarray(psf_size, dtype=np.int32)
    new_psf = circshift(new_psf, -np.floor(psf_size / 2))

    otf = np.fft.fftn(new_psf)

    if show_plot:
        surf_plot(new_psf)
        surf_plot(otf)

    return np.complex64(otf)


if __name__ == "__main__":
    psf = np.asarray([[-1, 1]])
    out_size = (28, 28)
    otfx = psf2otf(psf, out_size, False)
    psf = np.asarray([[-1], [1]])
    out_size = (28, 28)
    otfy = psf2otf(psf, out_size, False)

    Denormin2 = np.square(abs(otfx)) + np.square(abs(otfy))
    x = np.linspace(0, 28, 28)
    y = np.linspace(0, 28, 28)
    z = Denormin2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.contour3D(x, y, z, 120)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('psf')
    plt.show()
