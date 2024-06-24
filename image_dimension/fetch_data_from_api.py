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

def dimensions(images):
    # Get the dimensions of the images
    dimensions = []
    for image in images:
        dimensions.append(image.size)
    return dimensions




if __name__ == "__main__":
    
    # URL to query
    # url = "http://www.artisanfurniture.net/wp-json/rest-product/get-ai-products?token=fer85s9e525df4g8e996nmu63225r3l22z200w2q5"


    #read the data from the text file
    with open("data.json", "r") as file:
        data = file.read()
    data = json.loads(data)


    #iterating throught the product info
    for item in data:
        #get the image url
        imageLinks = item["romanceDetails"]["_product_image_gallery"]


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


        #create imagelinks
        if len(imagePaths) > 0:
            pass


