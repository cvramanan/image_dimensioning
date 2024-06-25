import cv2
import numpy as np



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
    # exit()

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







FURNITURE_IMAGE_PATH = 'data/fur/out.png'

image = read_transparent_png(FURNITURE_IMAGE_PATH)


# show the image
cv2.imshow('image', image)
cv2.waitKey(0)