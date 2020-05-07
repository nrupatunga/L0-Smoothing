"""
File: L0Smoothing.py
Author: Nrupatunga
Email: nrupatunga.s@byjus.com
Github: https://github.com/nrupatunga
Description: Implementation of the following paper

Paper details
Title:'Image Smoothing via L0 Gradient Minimization'
Link: http://www.cse.cuhk.edu.hk/~leojia/papers/L0smooth_Siggraph_Asia2011.pdf
"""
from typing import Optional

import cv2
import numpy as np

from psf2otf import psf2otf


class L0Smoothing:

    """Docstring for L0Smoothing. """

    def __init__(self, img_path: str,
                 param_lambda: Optional[float] = 2e-2,
                 param_kappa: Optional[float] = 2.0):
        """Initialization of parameters """
        self._lambda = param_lambda
        self._kappa = param_kappa
        self._img_path = img_path
        self._beta_max = 1e5

    def run(self):
        """L0 smoothing imlementation"""
        img = cv2.imread(self._img_path)
        S = cv2.normalize(img, None, alpha=0, beta=1,
                          norm_type=cv2.NORM_MINMAX,
                          dtype=cv2.CV_32F)
        if S.ndim < 3:
            S = S[..., np.newaxis]

        N, M, D = S.shape

        beta = 2 * self._lambda

        psf = np.asarray([[-1, 1]])
        out_size = (N, M)
        otfx = psf2otf(psf, out_size)
        psf = np.asarray([[-1], [1]])
        otfy = psf2otf(psf, out_size)

        Normin1 = np.fft.fft2(np.squeeze(S), axes=(0, 1))
        Denormin2 = np.square(abs(otfx)) + np.square(abs(otfy))
        if D > 1:
            Denormin2 = Denormin2[..., np.newaxis]
            Denormin2 = np.repeat(Denormin2, 3, axis=2)

        while beta < self._beta_max:
            Denormin = 1 + beta * Denormin2

            h = np.diff(S, axis=1)
            last_col = S[:, 0, :] - S[:, -1, :]
            last_col = last_col[:, np.newaxis, :]
            h = np.hstack([h, last_col])

            v = np.diff(S, axis=0)
            last_row = S[0, ...] - S[-1, ...]
            last_row = last_row[np.newaxis, ...]
            v = np.vstack([v, last_row])

            grad = np.square(h) + np.square(v)
            if D > 1:
                grad = np.sum(grad, axis=2)
                idx = grad < (self._lambda / beta)
                idx = idx[..., np.newaxis]
                idx = np.repeat(idx, 3, axis=2)
            else:
                grad = np.sum(grad, axis=2)
                idx = grad < (self._lambda / beta)

            h[idx] = 0
            v[idx] = 0

            h_diff = -np.diff(h, axis=1)
            first_col = h[:, -1, :] - h[:, 0, :]
            first_col = first_col[:, np.newaxis, :]
            h_diff = np.hstack([first_col, h_diff])

            v_diff = -np.diff(v, axis=0)
            first_row = v[-1, ...] - v[0, ...]
            first_row = first_row[np.newaxis, ...]
            v_diff = np.vstack([first_row, v_diff])

            Normin2 = h_diff + v_diff
            Normin2 = beta * np.fft.fft2(Normin2, axes=(0, 1))

            FS = np.divide(np.squeeze(Normin1) + np.squeeze(Normin2),
                           Denormin)
            S = np.real(np.fft.ifft2(FS, axes=(0, 1)))
            if False:
                S_new = S * 256
                S_new = S_new.astype(np.uint8)
                cv2.imshow('L0-Smooth', S_new)
                cv2.waitKey(0)

            if S.ndim < 3:
                S = S[..., np.newaxis]
            beta = beta * self._kappa

        return S


if __name__ == "__main__":
    img_path = './pflower.jpg'
    img = cv2.imread(img_path)
    S = L0Smoothing(img_path, param_lambda=0.01).run()
    S = np.squeeze(S)
    S = cv2.normalize(S, None, alpha=0, beta=255,
                      norm_type=cv2.NORM_MINMAX,
                      dtype=cv2.CV_32F)
    S = S.astype(np.uint8)
    cv2.imshow('Input', img)
    cv2.imshow('L0-Smooth', S)
    cv2.waitKey(0)
    cv2.imwrite('output_python.png', S)
