import numpy as np


def find_vertical_seam(energy: np.ndarray) -> np.ndarray:
    """
    Find the vertical seam with the lowest total energy.
    Returns one column index per row.
    """
    height, width = energy.shape

    cost = energy.copy()
    paths = np.zeros((height, width), dtype=np.int32)

    for y in range(1, height):
        for x in range(width):
            previous_x_options = [x]

            if x > 0:
                previous_x_options.append(x - 1)

            if x < width - 1:
                previous_x_options.append(x + 1)

            best_previous_x = min(
                previous_x_options,
                key=lambda px: cost[y - 1, px],
            )

            cost[y, x] += cost[y - 1, best_previous_x]
            paths[y, x] = best_previous_x

    seam = np.zeros(height, dtype=np.int32)
    seam[-1] = np.argmin(cost[-1])

    for y in range(height - 2, -1, -1):
        seam[y] = paths[y + 1, seam[y + 1]]

    return seam
