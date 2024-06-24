import cv2
import numpy as np


INPUT_IMAGE = 'data/cropped_mode.png'


# Load the image
image  = cv2.imread(INPUT_IMAGE)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray[ gray > 100 ] = 255

#convert the gray back to colour image
image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

#show the image
cv2.imshow('image', image)
cv2.waitKey(0)

#save the image
cv2.imwrite('data/cropped_mode_denoised.png', image)
cv2.destroyAllWindows()
