import cv2
from PIL import Image
import io
import math

def thresholdFilter(currentFrame, delta):
    img = currentFrame

    frame_height, frame_width, channels = img.shape

    blueChannel, greenChannel, redChannel = cv2.split(img)

    for height in range(0, frame_height):
        for width in range(0, frame_width):
            color = redChannel[height][width]
            if color <= 50 + delta:
                color = 0
            elif color <= 100 + delta:
                color = 25
            elif color <= 150 + delta:
                color = 180
            elif color <= 200 + delta:
                color = 210
            else:
                color = 255
            redChannel[height][width] = color

    for height in range(0, frame_height):
        for width in range(0, frame_width):
            color = greenChannel[height][width]
            # print(height, width)
            if color <= 50 + delta:
                color = 0
            elif color <= 100 + delta:
                color = 25
            elif color <= 150 + delta:
                color = 180
            elif color <= 200 + delta:
                color = 210
            else:
                color = 255
            greenChannel[height][width] = color

    for height in range(0, frame_height):
        for width in range(0, frame_width):
            color = blueChannel[height][width]
            if color <= 50 + delta:
                color = 0
            elif color <= 100 + delta:
                color = 25
            elif color <= 150 + delta:
                color = 180
            elif color <= 200 + delta:
                color = 210
            else:
                color = 255
            blueChannel[height][width] = color

    merge_image = cv2.merge([blueChannel, redChannel, greenChannel])

    return merge_image

def cv2ToGUI(currenFrame):
    scale = 450 / currenFrame.shape[1]
    dim = (round(currenFrame.shape[1] * scale), round(currenFrame.shape[0] * scale))

    correctFrame = cv2.resize(currenFrame, dim)

    img = Image.fromarray(correctFrame)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()

    return imgbytes