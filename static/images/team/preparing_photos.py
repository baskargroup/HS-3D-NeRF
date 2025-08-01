#!/usr/bin/env python3
import argparse
from PIL import Image, ImageDraw

def crop_to_circle_with_border(input_path, output_path, border=10):
    """
    Crop the input image to a circle and add a white border.

    Parameters:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resulting image.
        border (int): Size of the white border in pixels.
    """
    # Open the input image and ensure it has an alpha channel.
    im = Image.open(input_path).convert("RGBA")
    width, height = im.size

    # Crop the image to a square using center crop.
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    im_cropped = im.crop((left, top, right, bottom))

    # Create a circular mask.
    mask = Image.new("L", (min_dim, min_dim), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, min_dim, min_dim), fill=255)

    # Apply the circular mask to the cropped image.
    im_circle = Image.new("RGBA", (min_dim, min_dim))
    im_circle.paste(im_cropped, (0, 0), mask=mask)

    # Determine the new dimensions to include the white border.
    final_size = min_dim + 2 * border

    # Create a new image with a white background.
    final_img = Image.new("RGBA", (final_size, final_size), "white")

    # Paste the circular image onto the center of the white background.
    final_img.paste(im_circle, (border, border), im_circle)

    # Save the final image.
    final_img.save(output_path)
    print(f"Saved circle-cropped image with border as '{output_path}'.")

def main():
    parser = argparse.ArgumentParser(description="Crop an image to a circle with a white border.")
    parser.add_argument("input", help="Path to the input image.")
    parser.add_argument("output", help="Path for the output image.")
    parser.add_argument("--border", type=int, default=10, help="Border size in pixels (default: 10)")
    
    args = parser.parse_args()
    crop_to_circle_with_border(args.input, args.output, border=args.border)

if __name__ == "__main__":
    main()

#Usage case
#python your_script.py input.jpg output.png --border 20
