import cv2
import numpy as np


def show_image(image, graph):
    if image.shape[1] > 450:
        scale = 450 / image.shape[1]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        img_bytes = cv2.imencode('.png', image)[1].tobytes()
        graph.erase()
        a_id = graph.draw_image(data=img_bytes, location=(0, int((450-image.shape[0])/2)))
        graph.send_figure_to_back(a_id)

    if image.shape[0] > 450:
        scale = 450 / image.shape[0]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        img_bytes = cv2.imencode('.png', image)[1].tobytes()
        graph.erase()
        a_id = graph.draw_image(data=img_bytes, location=(int((450-image.shape[1])/2), 0))
        graph.send_figure_to_back(a_id)

    if image.shape[0] < 450 and image.shape[1] < 450:
        if image.shape[0] > image.shape[1]:
            scale = 450 / image.shape[0]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
            img_bytes = cv2.imencode('.png', image)[1].tobytes()
            graph.erase()
            a_id = graph.draw_image(data=img_bytes, location=(int((450 - image.shape[1]) / 2), 0))
            graph.send_figure_to_back(a_id)
        else:
            scale = 450 / image.shape[1]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
            img_bytes = cv2.imencode('.png', image)[1].tobytes()
            graph.erase()
            a_id = graph.draw_image(data=img_bytes, location=(0, int((450 - image.shape[0]) / 2)))
            graph.send_figure_to_back(a_id)

def splitFilter(currentFrame, choosenChannel, redImg=None):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)

    redChannel, greenChannel, blueChannel = cv2.split(currentFrame)
    print("splited channel")

    if (choosenChannel == 0):
        return redChannel
    elif (choosenChannel == 1):
        return greenChannel
    elif (choosenChannel == 2):
        return blueChannel
    else:
        return currentFrame

def BrightContrBlur(img, contrastValue, brightnessValue, gaussianValue):
    imgResult = cv2.addWeighted(img, contrastValue, img, 0, brightnessValue)

    imgResult = cv2.GaussianBlur(src=imgResult, ksize=(gaussianValue, gaussianValue), sigmaX=0, sigmaY=0,
                                      borderType=cv2.BORDER_DEFAULT)

    return imgResult