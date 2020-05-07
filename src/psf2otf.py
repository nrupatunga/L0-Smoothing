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


def psf2otf(psf: np.ndarray, out_size: tuple):
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
    return np.complex64(otf)


if __name__ == "__main__":
    psf = np.asarray([[-1, 1]])
    out_size = (494, 475)
    psf2otf(psf, out_size)
