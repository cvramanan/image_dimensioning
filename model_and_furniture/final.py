import cv2
import numpy as np
import os
import time

def read_transparent_png(filename):
    """
    Read a transparent PNG file and render it on a white background.

    Parameters:
    filename (str): The path to the PNG file.

    Returns:
    np.ndarray: The image rendered on a white background.
    """
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

def model_with_furniture(model_image_path, furniture_image_path, furniture_height=100, furniture_width=70):
    """
    Combine a model image with a furniture image, scaling the furniture to the given dimensions.

    Parameters:
    model_image_path (str): The path to the model image.
    furniture_image_path (str): The path to the furniture image.
    furniture_height (int): The desired height of the furniture in cm. Default is 100 cm.
    furniture_width (int): The desired width of the furniture in cm. Default is 70 cm.

    Returns:
    np.ndarray: The combined image with the model and furniture.
    """
    # Load the model image
    model_image = cv2.imread(model_image_path)

    #filter out the furniture
    os.system('backgroundremover -i' + furniture_image_path + ' -o' + "output.png")

    # Load and process the furniture image
    furniture_image = read_transparent_png('output.png')

    # Constants
    MODEL_HEIGHT_CM = 170

    # Calculate height ratio
    height_ratio = model_image.shape[0] / MODEL_HEIGHT_CM

    # Scale the furniture image
    furniture_image = cv2.resize(furniture_image, 
                                 (int(furniture_width * height_ratio), 
                                  int(furniture_height * height_ratio)))

    # Create a canvas with furniture and model size dynamically
    canvas_height , canvas_width = model_image.shape[0], int(model_image.shape[1] + furniture_image.shape[1]*1.5)


    canvas = np.ones((canvas_height, canvas_width, 3), np.uint8) * 255

    # Place the model image on the canvas at the bottom-left corner
    canvas[canvas.shape[0] - model_image.shape[0]:, :model_image.shape[1]] = model_image

    # Place the furniture image on the canvas at the bottom-center
    x_offset = int((canvas.shape[1] - furniture_image.shape[1]) / 2)
    canvas[canvas.shape[0] - furniture_image.shape[0]:, x_offset:x_offset + furniture_image.shape[1]] = furniture_image

    return canvas

if __name__ == "__main__":
    # Define image paths
    model_image_path = 'data/hi-res.jpeg'
    furniture_image_path = 'data/IN3527-1.jpg'

    # Combine model and furniture images
    output_image = model_with_furniture(model_image_path, furniture_image_path, 132, 145)

    #write the image to the data folder with random name with time.time
    cv2.imwrite('data/' + str(time.time()) + '.png', output_image)


    # Display the result
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
