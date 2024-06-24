from PIL import Image
import os
import cv2
import numpy as np

def create_gif(image_list, output_path, duration=1000):
    """
    Create a GIF from a list of images.
    
    :param image_list: List of file paths to the images.
    :param output_path: Output path for the GIF.
    :param duration: Delay between frames in milliseconds (default is 1000ms or 1 second).
    """
    # Load images
    images = [Image.open(image).resize((500, 500)) for image in image_list]
    
    # Save as GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)


INPUTPATH  = "./data/teeth_demo/"

# Get all the files in the directory
files = os.listdir(INPUTPATH)

# Filter out only the image files
image_files = [file for file in files if file.endswith('.png')]

# Sort the image files by name
image_files.sort()

# Create a list of file paths to the images
image_list = [os.path.join(INPUTPATH, file) for file in image_files]

# Output path for the GIF
output_path = 'output.gif'





# Example usage


create_gif(image_list, output_path, duration=1000)
