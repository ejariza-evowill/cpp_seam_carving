import numpy as np


def compute_energy(image: np.ndarray) -> np.ndarray:
    """
    Compute a simple energy map using pixel gradients.
    Higher energy = more important pixel.
    """
    gray = image.mean(axis=2)

    dy = np.abs(np.roll(gray, -1, axis=0) - np.roll(gray, 1, axis=0))
    dx = np.abs(np.roll(gray, -1, axis=1) - np.roll(gray, 1, axis=1))

    return dx + dy
