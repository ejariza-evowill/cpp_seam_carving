import argparse

import numpy as np
from PIL import Image

from seam_carve_width import seam_carve_width


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reduce an image width using vertical seam carving.",
    )
    parser.add_argument(
        "image",
        help="Path to the input image.",
    )
    parser.add_argument(
        "--output",
        default="output.png",
        help="Path to the output image. Defaults to output.png.",
    )
    parser.add_argument(
        "--pixels-to-remove",
        type=int,
        default=50,
        help="Number of vertical seams to remove. Defaults to 50.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = Image.open(args.image).convert("RGB")
    image_array = np.array(image)

    carved = seam_carve_width(
        image=image_array,
        pixels_to_remove=args.pixels_to_remove,
    )

    Image.fromarray(carved).save(args.output)
    print(f"Saved seam-carved image to {args.output}")


if __name__ == "__main__":
    main()
