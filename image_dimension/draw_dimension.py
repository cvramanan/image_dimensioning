import cv2
import numpy as np
from print_text import add_text
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont


def add_text(image_path, text, x, y, font_path, font_size, color):
    font = ImageFont.truetype(font_path, font_size)
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    draw.text((x, y), text, font=font, fill=color)
    #convert the image from pillow to opencv
    image = im.getim()
    #return the image
    return image

def drawDimension(straightImage, sideImage, height, width, depth, canvas_size=50):
    """
    Draws dimensions on the given images.

    Parameters:
    straightImage (numpy.ndarray): The straight image.
    sideImage (numpy.ndarray): The side image.
    height (int): The height of the object in cm.
    width (int): The width of the object in cm.
    depth (int): The depth of the object in cm.
    canvas_size (int, optional): The size of the canvas for padding. Defaults to 50.

    Returns:
    tuple: The straight and side images with dimensions drawn.
    """

    # Draw the dimensions for straight image
    image = cv2.copyMakeBorder(straightImage, canvas_size, canvas_size, canvas_size, canvas_size, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    presentationImage = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    center_x = x + w // 2
    center_y = y + h // 2

    Y_CANVAS = 30
    Y_CANVAS_TEXT = 45
    X_CANVAS = -20
    X_CANVAS_TEXT = -100

    #write the image as text sample
    cv2.imwrite("data/temp.png", presentationImage)
    # cv2.putText(presentationImage, f"{width}cm", (x + X_CANVAS_TEXT, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    presentationImage = add_text("data/temp.png", f"{width}cm", x + X_CANVAS_TEXT, center_y, "data/font/BodoniXT.ttf", 25, (0, 0, 0))
    cv2.imwrite("data/temp.png", presentationImage)
    # cv2.putText(presentationImage, f"{height}cm", (center_x, y + Y_CANVAS_TEXT+h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    presentationImage = add_text("data/temp.png", f"{height}cm", center_x, y + Y_CANVAS_TEXT+h, "data/font/BodoniXT.ttf", 25, (0, 0, 0))


    cv2.arrowedLine(presentationImage, (x, y +h+ Y_CANVAS), (x + w, y +h+ Y_CANVAS), (0, 0, 0), 2, tipLength=0.02)
    cv2.arrowedLine(presentationImage, (x + w, y +h+ Y_CANVAS), (x, y +h+ Y_CANVAS), (0, 0, 0), 2, tipLength=0.02)


    cv2.arrowedLine(presentationImage, (x + X_CANVAS, y + h), (x + X_CANVAS, y), (0, 0, 0), 2, tipLength=0.02)
    cv2.arrowedLine(presentationImage, (x + X_CANVAS, y), (x + X_CANVAS, y + h), (0, 0, 0), 2, tipLength=0.02)

    straightImage = presentationImage.copy()

    # Draw the dimensions for side image
    image = cv2.copyMakeBorder(sideImage, canvas_size, canvas_size, canvas_size, canvas_size, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    presentationImage = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    center_x = x + w // 2
    center_y = y + h // 2

    Y_CANVAS = 20
    Y_CANVAS_TEXT = 35

    # cv2.putText(presentationImage, f"{depth}cm", (center_x, y + h + Y_CANVAS_TEXT), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    #write the image as text sample
    cv2.imwrite("data/temp.png", presentationImage)
    presentationImage = add_text("data/temp.png", f"{depth}cm", center_x, y + h + Y_CANVAS_TEXT, "data/font/BodoniXT.ttf", 25, (0, 0, 0))
    cv2.arrowedLine(presentationImage, (x, y + h + Y_CANVAS), (x + w, y + h + Y_CANVAS), (0, 0, 0), 2, tipLength=0.02)
    cv2.arrowedLine(presentationImage, (x + w, y + h + Y_CANVAS), (x, y + h + Y_CANVAS), (0, 0, 0), 2, tipLength=0.02)

    sideImage = presentationImage.copy()

    #hstack the images
    presentationImage = np.hstack((straightImage, sideImage))

    return presentationImage

if __name__ == "__main__":
    # Load the images
    straightImage_image_path = 'data/fur2/IN038_10.png'
    straightImage = cv2.imread(straightImage_image_path)
    sideImage_image_path = 'data/fur2/IN038_7.png'
    sideImage = cv2.imread(sideImage_image_path)

    # Draw the dimensions
    saveImage = drawDimension(straightImage, sideImage, 30, 90, 40, 100)

    # Save the images with dimensions
    cv2.imwrite(straightImage_image_path.split('.')[0] + '_dimensioned.png', saveImage)
