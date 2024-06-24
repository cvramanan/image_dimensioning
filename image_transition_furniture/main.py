import cv2
import numpy as np
import os
import json
import requests
from PIL import Image
from io import BytesIO
from halo import Halo






#creating a temporary directory to store the images
os.makedirs("temp", exist_ok=True)
#create an output directory to store the .gif files
os.makedirs("output", exist_ok=True)

def create_gif(image_list, output_path, duration=1000):
    """
    Create a GIF from a list of images using a canvas of the size of the first image.
    
    :param image_list: List of file paths to the images.
    :param output_path: Output path for the GIF.
    :param duration: Delay between frames in milliseconds (default is 1000ms or 1 second).
    """
    # Load the first image to get the size of the canvas
    first_image = Image.open(image_list[0])
    canvas_size = first_image.size
    
    # Create a list to hold images placed on the canvas
    images_on_canvas = []
    
    for image_path in image_list:
        # Open the image
        img = Image.open(image_path)
        
        # Create a new image with a white background and the same size as the canvas
        canvas = Image.new('RGB', canvas_size, (255, 255, 255))
        
        # Calculate the position to paste the image on the canvas (centered)
        position = ((canvas_size[0] - img.size[0]) // 2, (canvas_size[1] - img.size[1]) // 2)
        
        # Paste the image onto the canvas
        canvas.paste(img, position)
        
        # Append the canvas with the image to the list
        images_on_canvas.append(canvas)
    
    # Save the list of images as a GIF
    images_on_canvas[0].save(output_path, save_all=True, append_images=images_on_canvas[1:], duration=duration, loop=0)




if __name__ == "__main__":
    
    # URL to query
    url = "http://www.artisanfurniture.net/wp-json/rest-product/get-ai-products?token=fer85s9e525df4g8e996nmu63225r3l22z200w2q5"

    spinner = Halo(text='Querying the API', spinner='dots')
    spinner.start()
    # Send a GET request to the URL
    response = requests.get(url,timeout=20)



    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        spinner.succeed("API query successful")
    #iterating throught the product info
    for item in data:
        #get the image url
        imageLinks = item["romanceDetails"]["_product_image_gallery"]
        spinner = Halo(text='Downloading images', spinner='dots')
        spinner.start()
        spinner.text = f"Downloading images for {item['romanceDetails']['_sku']}"
        # if item['romanceDetails']['_sku'] != "IN3662" or item['romanceDetails']['_sku'] != "IN3634":
        #     continue
        #Download the image
        imagePaths = []
        for i, imageLink in enumerate(imageLinks):
            try:
                response = requests.get(imageLink,timeout=5)
            except requests.exceptions.Timeout:
                print(f"Timeout error for {imageLink}")
                continue
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                #resize the images to 500x500
                image = image.resize((500, 500))
                image.convert('RGB').save(f"temp/{item['romanceDetails']['_sku']}_{i}.png")
                imagePaths.append(f"temp/{item['romanceDetails']['_sku']}_{i}.png")
            else:
                print(f"Failed to download image {imageLink}")

        spinner.text = f"Creating GIF for {item['romanceDetails']['_sku']}"
        #create imagelinks
        if len(imagePaths) > 0:
            create_gif(imagePaths, f"output/{item['romanceDetails']['_sku']}.gif", duration=1000)

        spinner.succeed(f"Created GIF for {item['romanceDetails']['_sku']}")
