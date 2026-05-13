import numpy as np

from src.compute_energy import compute_energy
from src.find_vertical_seam import find_vertical_seam
from src.measure_time import measure_time
from src.remove_vertical_seam import remove_vertical_seam


@measure_time
def seam_carve_width(image: np.ndarray, pixels_to_remove: int) -> np.ndarray:
    """
    Remove N vertical seams from the image.
    """
    if pixels_to_remove < 0:
        raise ValueError("pixels_to_remove must be non-negative")

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("image must be an RGB image with shape (height, width, 3)")

    if pixels_to_remove >= image.shape[1]:
        raise ValueError("pixels_to_remove must be smaller than the image width")

    carved = image.copy()


    for _ in range(pixels_to_remove):
        energy = compute_energy(carved)
        seam = find_vertical_seam(energy)
        carved = remove_vertical_seam(carved, seam)

    return carved
