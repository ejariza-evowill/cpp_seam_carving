import numpy as np


def remove_vertical_seam(image: np.ndarray, seam: np.ndarray) -> np.ndarray:
    """
    Remove one pixel from each row according to the seam.
    """
    height, width, channels = image.shape
    output = np.zeros((height, width - 1, channels), dtype=image.dtype)

    for y in range(height):
        x = seam[y]

        output[y, :, :] = np.concatenate(
            [image[y, :x, :], image[y, x + 1 :, :]],
            axis=0,
        )

    return output
