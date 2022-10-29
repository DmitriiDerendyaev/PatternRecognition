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


def splitFilter(currentFrame, choosenChannel):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)

    redChannel, greenChannel, blueChannel = cv2.split(currentFrame)

    if (choosenChannel == 0):
        return redChannel
    elif (choosenChannel == 1):
        return greenChannel
    elif (choosenChannel == 2):
        return blueChannel
    else:
        print("Out of bound")
        return currentFrame

def BrightContrBlur(img, contrastValue, brightnessValue, gaussianValue):
    imgResult = cv2.addWeighted(img, contrastValue, img, 0, brightnessValue)

    imgResult = cv2.GaussianBlur(imgResult, (gaussianValue, gaussianValue),0)

    return imgResult

def preImage(event, values, startFrame):


    brightnessValue = values["-BrightnessValue-"]
    contrastValue = values["-ContrastValue-"]
    gaussianValue = int((values["-BlurValue-"] * 2) - 1)

    # print(brightnessValue, contrastValue, gaussianValue)

    img_before = BrightContrBlur(startFrame, contrastValue, brightnessValue, gaussianValue)

    if values["-MonoChannel-"]:
        imgToPrint = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    elif values["-RedChannel-"]:
        imgToPrint = splitFilter(img_before, 0)
    elif values["-GreenChannel-"]:
        imgToPrint = splitFilter(img_before, 1)
    elif values["-BlueChannel-"]:
        imgToPrint = splitFilter(img_before, 2)
    else:
        imgToPrint = startFrame

    if values["-ThresholdBinary-"]:
        thresholdValue = int(values["-ThresholdValue-"])
        ret, imgToPrintTH = cv2.threshold(imgToPrint, thresholdValue, 255, cv2.THRESH_BINARY)

        return imgToPrintTH
    else:
        return imgToPrint
