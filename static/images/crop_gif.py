#!/usr/bin/env python3
import argparse
from PIL import Image, ImageSequence

def process_frames_and_durations(im):
    """
    Processes an optimized GIF to composite full frames and returns a list
    of frames (as RGBA images) and their corresponding durations.
    """
    palette = im.getpalette()
    frames = []
    durations = []
    last_frame = None
    try:
        while True:
            im.putpalette(palette)
            new_frame = im.convert('RGBA')
            if im.tell() == 0:
                composite = new_frame
            else:
                # Create a composite of the previous full frame and the new frame.
                composite = last_frame.copy()
                composite.alpha_composite(new_frame)
            frames.append(composite)
            durations.append(im.info.get('duration', 100))  # Default duration is 100 ms.
            last_frame = composite
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return frames, durations

def crop_gif(input_path, output_path, left, top, right, bottom):
    with Image.open(input_path) as im:
        width, height = im.size
        # Validate that crop coordinates are within full image boundaries.
        if left < 0 or top < 0 or right > width or bottom > height:
            raise ValueError(
                f"Crop coordinates must be within the image boundaries: (0, 0) to ({width}, {height})"
            )
        
        # Process (deoptimize) frames to get full images and their durations.
        frames, durations = process_frames_and_durations(im)
        cropped_frames = []
        for frame in frames:
            # Crop the full-frame image.
            cropped = frame.crop((left, top, right, bottom))
            # Convert the cropped frame to palette mode (required for GIF output).
            cropped_p = cropped.convert("P", palette=Image.ADAPTIVE)
            cropped_frames.append(cropped_p)
        
        # Preserve loop info (default 0 means infinite looping)
        loop = im.info.get('loop', 0)

    cropped_frames[0].save(
        output_path,
        save_all=True,
        append_images=cropped_frames[1:],
        duration=durations,
        loop=loop,
        optimize=False,
        disposal=2  # Use disposal method 2 for better animation compatibility
    )
    print(f"Cropped GIF saved as '{output_path}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Crop an animated GIF by compositing full frames and applying a crop."
    )
    parser.add_argument("input", help="Input GIF file path")
    parser.add_argument("output", help="Output cropped GIF file path")
    parser.add_argument("--left", type=int, required=True, help="Left coordinate for cropping")
    parser.add_argument("--top", type=int, required=True, help="Top coordinate for cropping")
    parser.add_argument("--right", type=int, required=True, help="Right coordinate for cropping")
    parser.add_argument("--bottom", type=int, required=True, help="Bottom coordinate for cropping")
    args = parser.parse_args()
    crop_gif(args.input, args.output, args.left, args.top, args.right, args.bottom)

if __name__ == "__main__":
    main()



# Usage case:
#python crop_gif.py input.gif cropped_output.gif --left 50 --top 50 --right 250 --bottom 250
