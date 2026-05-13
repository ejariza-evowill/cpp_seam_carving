# Seam Carving CLI

This project reduces an image's width with vertical seam carving. The CLI reads an input image, removes a configurable number of low-energy (or low-information) vertical seams, and writes the result to a new image file.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run the CLI

The CLI entrypoint is `main.py`.

```bash
python main.py <image_path>
```

Example:

```bash
python main.py image.png
```

By default, the result is saved as `output.png`.

To choose a different output path:

```bash
python main.py image.png --output carved.png
```

You can also control how many columns are removed:

```bash
python main.py image.png --pixels-to-remove 50 --output carved.png
```

## Implementation Details

The seam-carving loop lives in `seam_carve_width.py`, and the helper functions are split into small modules under `src/`:

- `src/compute_energy.py`
- `src/find_vertical_seam.py`
- `src/remove_vertical_seam.py`

### `compute_energy`

`compute_energy(image)` builds an energy map from the input RGB image:

In this case we understand the energy as the local contrast of each pixel (in other words, the rate of change in intensity), which is a common choice for seam carving. The algorithm works as follows:

- It converts the image to grayscale by averaging the three color channels.
- It estimates horizontal and vertical gradients with `np.roll`. `np.roll` shifts the image in a specified direction, allowing us to compute differences between neighboring pixels without explicit loops.
- It sums the absolute x and y gradients to produce one energy value per pixel.

Pixels with larger local contrast receive higher energy, which makes them less likely to be removed.

### `find_vertical_seam`

`find_vertical_seam(energy)` uses dynamic programming to locate the lowest-cost top-to-bottom seam:

- `cost[y, x]` stores the minimum cumulative energy to reach pixel `(y, x)` following the least "informative" path (i.e the variance of intensity along the path is minimal).
- `paths[y, x]` stores which column in the previous row produced that minimum.
- For each pixel, the algorithm checks the reachable pixels from the row above: directly above, above-left, and above-right.
- After filling the table, it starts from the minimum cost in the last row and backtracks through `paths` to reconstruct the seam.

The result is a one-dimensional array with one column index per row.

### `remove_vertical_seam`

`remove_vertical_seam(image, seam)` creates a new image that is one column narrower:

- For each row, it removes the pixel at the seam column.
- The pixels before and after that column are concatenated together.

This preserves the row order while shrinking the width by exactly one pixel.

### `seam_carve_width`

`seam_carve_width(image, pixels_to_remove)` repeats the seam removal loop:

1. Compute the current energy map.
2. Find the lowest-energy vertical seam.
3. Remove that seam.
4. Repeat until the requested number of seams has been removed.

The function validates that:

- `pixels_to_remove` is non-negative.
- The image is RGB with shape `(height, width, 3)`.
- The number of pixels to remove is smaller than the image width.

## Benchmarking
I ran the seam carving on a regular laptop (My computer), removing a single vertical seam, and got the following results:

image_small.png: 0.1692s
image_medium.png: 2.5191s
image_large.png: 11.0797s

You can expect the time to grow linearly with the number of pixels or seams removed (ten seams in image_medium.png would take about 25 seconds and so on). 

## Notes

- This implementation only reduces width by removing vertical seams.
- It does not preserve an alpha channel because images are converted to RGB before processing.
- Because the energy map is recomputed after every seam removal, the output adapts to the updated image structure after each step.
