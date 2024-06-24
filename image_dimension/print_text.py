from __future__ import print_function
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw
import PILasOPENCV as ImageFont
import cv2
import numpy as np
# was: from PIL import Image, ImageDraw, ImageFont

# font = ImageFont.truetype("data/font/BodoniXT.ttf", 18)
# print(font)
# im = Image.open("data/fur1/IN015_0.png")
# draw = ImageDraw.Draw(im)
# text = "Lena's image"
# draw.text((249,455), text, font=font, fill=(0, 0, 0))
# # in PIL:
# # print(font.getsize(text))
# # mask = font.getmask(text)
# print(ImageFont.getsize(text, font))
# mask = ImageFont.getmask(text, font)
# print(type(mask))
# cv2.imshow("mask", mask)
# im.show()

#create a funtion with the above code
def add_text(image_path, text, x, y, font_path, font_size, color):
    font = ImageFont.truetype(font_path, font_size)
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    draw.text((x, y), text, font=font, fill=color)
    #convert the image from pillow to opencv
    image = im.getim()
    #return the image
    return image

if __name__ == "__main__":
    #read the image
    
    image = add_text("data/fur1/IN015_0.png", "Lena's image", 249, 455, "data/font/BodoniXT.ttf", 18, (0, 0, 0))
    #show the image
    cv2.imshow("image", image)
    cv2.waitKey(0)