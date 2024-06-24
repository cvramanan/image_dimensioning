import cv2
import numpy as np


# IMAGE_PATH = 'output.png'

# #create a normal window
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# # Load the image
# image = cv2.imread(IMAGE_PATH)

# #convert the image to grayscale
# gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

# #threshold the image
# _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

# #apply contours detection
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# #contour with max area
# c = max(contours, key=cv2.contourArea)

# thresh = thresh.copy()*0


# #draw the contour
# cv2.drawContours(thresh, [c], -1, (255), -1)


# # Taking a matrix of size 5 as the kernel 
# kernel = np.ones((5, 5), np.uint8) 
# #smooth the edges
# thresh = cv2.erode(thresh, kernel, iterations=2)



# #filter only the threshold region of the image
# image = cv2.bitwise_and(image, image, mask=thresh)

# #change the background to white
# image[image == 0] = 255






# #display the image
# cv2.imshow('image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#create a function to remove the background
def cleanBagImage(image):
    #convert the image to grayscale
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

    #threshold the image
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    #apply contours detection
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #contour with max area
    c = max(contours, key=cv2.contourArea)

    thresh = thresh.copy()*0


    #draw the contour
    cv2.drawContours(thresh, [c], -1, (255), -1)


    # Taking a matrix of size 5 as the kernel 
    kernel = np.ones((5, 5), np.uint8) 
    #smooth the edges
    thresh = cv2.erode(thresh, kernel, iterations=2)



    #filter only the threshold region of the image
    image = cv2.bitwise_and(image, image, mask=thresh)

    #change the background to white
    image[image == 0] = 255

    return image