from PIL import Image, ImageChops

def trim_whitespace(input_path, output_path):
    with Image.open(input_path) as im:
        # Create a background the same size/color as a corner pixel
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        # Find the difference
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            # Crop the image to the bounding box
            trimmed_im = im.crop(bbox)
            trimmed_im.save(output_path)
            
# Example usage:
trim_whitespace("apricot_sc_render.gif", "apricot_trimmed.gif")
