import cv2
import numpy as np


INPUT_IMAGE = 'data/fur2.jpeg'

#read the image
image  = cv2.imread(INPUT_IMAGE)

#find the center of the image
#thershold the image with 255 white pixels
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)





#invert the image
thresh = cv2.bitwise_not(thresh)

#do a bitwise and operation with the original image
image = cv2.bitwise_and(image, image, mask=thresh)

#show the image
cv2.imshow('image', image)
cv2.waitKey(0)


