import cv2
import numpy as np
import os
from reading_alfa_channel_image import cleanBagImage



CAVAS_IMG_PATH = 'data/image.jpeg'
MODEL_IMG_PATH = 'data/hi-res.jpeg'
FURNITURE_IMG_PATH = 'data/fur1.jpeg'






#model height in cm
MODEL_HEIGHT = 170


# Load the image
canvasImage = cv2.imread(CAVAS_IMG_PATH)

#read the width and height of the image
height, width = canvasImage.shape[:2]

#create a new image with the same width and height
canvas = np.ones((height, width, 3), np.uint8)*255

#read the model image
modelImage = cv2.imread(MODEL_IMG_PATH)

#scale the model image to the height of the canvas
modelImage = cv2.resize(modelImage, (int(modelImage.shape[1]*height/modelImage.shape[0]), height))

#model height to pixel ratio
RATIO = modelImage.shape[0]/MODEL_HEIGHT

#insert the model image into the canvas image in the left bottom corner
leftBorderMovement = 10
canvas[height-modelImage.shape[0]:, leftBorderMovement:leftBorderMovement+modelImage.shape[1]] = modelImage

#show the image
# cv2.imshow('image', canvas)
# cv2.waitKey(0)


#furniture image
furnitureImage = cv2.imread(FURNITURE_IMG_PATH)

#remove the white background
os.system('backgroundremover -i' + FURNITURE_IMG_PATH + ' -o' + "output.png")

#read the furniture image
furnitureImage = cv2.imread('output.png')
furnitureImage = cleanBagImage(furnitureImage)

#show the image
# cv2.imshow('image', furnitureImage)
# cv2.waitKey(0)
# exit()


#furniture dimension in cm
TEMP_FACTOR = 3
FURNITURE_HEIGHT = 100*TEMP_FACTOR
FURNITURE_WIDTH = 80*TEMP_FACTOR


#furniture height to pixel ratio
furHeight = int(FURNITURE_HEIGHT*RATIO)
furWidth = int(FURNITURE_WIDTH*RATIO)



#rescale the furniture image
furnitureImage = cv2.resize(furnitureImage, (furWidth, furHeight))


#insert the furniture image into the canvas image in the bottom middle
bottomMiddle = (width-furWidth)//2
canvas[height-furHeight:, bottomMiddle:bottomMiddle+furWidth] = furnitureImage

#show the image
# cv2.imshow('image', canvas)
# cv2.waitKey(0)

#save the image to output
os.makedirs('./data/output', exist_ok=True)
cv2.imwrite('data/output/canvas_arrangement.png', canvas)

