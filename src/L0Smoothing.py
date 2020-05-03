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


class L0Smoothing:

    """Docstring for L0Smoothing. """

    def __init__(self, img_path: str,
                 param_lambda: float,
                 param_kappa: float):
        """Initialization of parameters """
        self._lambda = param_lambda
        self._kappa = param_kappa
        self._img_path = img_path
        self._beta_max = 1e5

    def run(self):
        """L0 smoothing imlementation"""
        pass
