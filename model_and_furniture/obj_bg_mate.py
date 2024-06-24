import cv2
import numpy as np


FURNITURE_IMAGE_PATH = 'data/fur/fur2.jpeg'

#create a window to show the image
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# Load the image
furnitureImage = cv2.imread(FURNITURE_IMAGE_PATH)

#show the image
cv2.imshow('image', furnitureImage)
cv2.waitKey(0)

#create a canvas of 1000 on all sides of the image with same background colour



