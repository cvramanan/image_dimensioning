import cv2
import numpy as np
import os

def read_transparent_png(filename):
    image_4channel = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    alpha_channel = image_4channel[:,:,3]

    #filter the alpha channel with contour detection and have only the contour with highest area
    _, thresh = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)
    alpha_channel = cv2.cvtColor(alpha_channel, cv2.COLOR_GRAY2BGR)
    for c in contours:
        if c is not cnt:
            alpha_channel = cv2.drawContours(alpha_channel, [c], -1, 0, -1)
    alpha_channel = cv2.cvtColor(alpha_channel, cv2.COLOR_BGR2GRAY)
    print(alpha_channel.shape)


    rgb_channels = image_4channel[:,:,:3]

    # White Background Image
    white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha factor
    alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor,alpha_factor,alpha_factor), axis=2)

    # Transparent Image Rendered on White Background
    base = rgb_channels.astype(np.float32) * alpha_factor
    white = white_background_image.astype(np.float32) * (1 - alpha_factor)
    final_image = base + white
    return final_image.astype(np.uint8)


FURNITURE_IMAGE_PATH = 'data/fur2.jpeg'

MODEL_IMAGE_PATH = 'data/hi-res.jpeg'




#create a function 
def modelWithFurniture(modelImageLocation,furnitureImageLocation,furnitureHeight = 100,furnitureWidth=70):
    # Load the model image
    modelImage = cv2.imread(modelImageLocation)



    #filter out the furniture
    os.system('backgroundremover -i' + furnitureImageLocation + ' -o' + "output.png")

    # Load the image
    furnitureImage = read_transparent_png('output.png')

    #model height in CM
    MODEL_HEIGHT = 170

    #model height in cm to pixel ratio
    HEIGHT_RATIO = modelImage.shape[0]/MODEL_HEIGHT


    #scale the furniture image with the HEIGHT_RATIO
    furnitureImage = cv2.resize(furnitureImage, (int(furnitureWidth*HEIGHT_RATIO), int(furnitureHeight*HEIGHT_RATIO)))


    #create a canvas of 572x748 pixels
    canvas = np.ones((1280, 1920, 3), np.uint8)*255

    #place the model image on the canvas on bottom left corner
    canvas[canvas.shape[0]-modelImage.shape[0]:, :modelImage.shape[1]] = modelImage

    #print the canvas and furniture image shape
    print(canvas.shape)
    print(furnitureImage.shape)


    #place the furniture image on the canvas on bottom center
    canvas[canvas.shape[0]-furnitureImage.shape[0]:, int((canvas.shape[1]-furnitureImage.shape[1])/2):int((canvas.shape[1]+furnitureImage.shape[1])/2)] = furnitureImage

    #return the image
    return canvas

if __name__ == "__main__":
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    outImage = modelWithFurniture('data/hi-res.jpeg','data/fur2.jpeg',100,100)

    #show the image 
    cv2.imshow('image', outImage)
    cv2.waitKey(0)