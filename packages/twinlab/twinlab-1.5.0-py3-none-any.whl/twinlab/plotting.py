# Third-party imports
import numpy as np
from typing import Optional


def get_blur_boundaries(n: int) -> np.ndarray:
    """
    Get boundaries for making a nice probability distribution of a Gaussian
    """
    frac = 1.0 / (2.0 * (n + 1.0))
    fmin, fmax = frac, 1.0 - frac
    f = np.linspace(fmin, fmax, n)
    dy = -np.sqrt(2.0) * np.log(f)
    return dy


def get_blur_alpha(n: int, alpha_mid: Optional[float] = 0.99) -> float:
    """
    Get a sensible alpha value for a given number of samples
    """
    alpha = 1.0 - (1.0 - alpha_mid) ** (1 / n)
    return alpha
