from math import cos, sin

import cv2
from PIL import Image
import io
import numpy as np
from numba import njit, jit, prange
import matplotlib.pyplot as plt
# import interface
# import PySimpleGUI as sg


def displayGraph(currentFrame, graph):
    scale = 350 / currentFrame.shape[1]
    dim = (round(currentFrame.shape[1] * scale), round(currentFrame.shape[0] * scale))

    correctFrame = cv2.resize(currentFrame, dim, interpolation=cv2.INTER_LINEAR)

    frame_height, frame_width, channels = correctFrame.shape

    img_bytes = cv2.imencode('.png', correctFrame)[1].tobytes()

    graph.erase()
    img = graph.draw_image(data=img_bytes, location=(450/2-frame_width/2, 450/2-frame_height/2))

    graph.send_figure_to_back(img)

def show_image(image, graph):
    if image.shape[0] < 450:
        scale = 450 / image.shape[1]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        img_bytes = cv2.imencode('.png', image)[1].tobytes()
        graph.erase()
        a_id = graph.draw_image(data=img_bytes, location=(0, int((450-image.shape[0])/2)-20))
        graph.send_figure_to_back(a_id)

    else:
        scale = 450 / image.shape[0]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
        img_bytes = cv2.imencode('.png', image)[1].tobytes()
        graph.erase()
        a_id = graph.draw_image(data=img_bytes, location=(int((450-image.shape[1])/2), 0))
        graph.send_figure_to_back(a_id)


def scallingFrameCV2(currentFrame, valueX, valueY, graph):
    scale = 350 / currentFrame.shape[1]
    dim = (round(currentFrame.shape[1] * scale), round(currentFrame.shape[0] * scale))

    currentFrame = cv2.resize(currentFrame, dim)

    width = int(currentFrame.shape[1] * valueX)
    height = int(currentFrame.shape[0] * valueY)
    dim = (width, height)
    correctFrame = cv2.resize(currentFrame, dim)

    frame_height, frame_width, channels = correctFrame.shape

    img_bytes = cv2.imencode('.png', correctFrame)[1].tobytes()

    graph.erase()
    EVA = graph.draw_image(data=img_bytes, location=(450 / 2 - frame_width / 2, 450 / 2 - frame_height / 2))

    graph.send_figure_to_back(EVA)

    return correctFrame


# @njit(nopython=True, parallel=True)
# @njit(parallel = True)
@njit(fastmath=True)
def scallingFrame(currentFrame, valueX, valueY):
    pictures = np.zeros(np.shape(currentFrame), np.uint8)

    for x in prange(pictures.shape[1]):
        for y in prange(pictures.shape[0]):
            scallingX = int(x * valueX)
            scallingY = int(y * valueY)
            if scallingX < pictures.shape[1]:
                if scallingY < pictures.shape[0]:
                    pictures[scallingY, scallingX] = currentFrame[y, x]

    return pictures


@njit(fastmath=True)
def shearingFrame(currentFrame, shift_X, shift_Y):
    pictures = np.zeros(np.shape(currentFrame), np.uint8)

    for x in prange(pictures.shape[1]):
        for y in prange(pictures.shape[0]):
            scallingX = int(x + shift_X * (currentFrame.shape[0] - y))
            scallingY = int(y + shift_Y * (currentFrame.shape[1] - x))
            if scallingX < pictures.shape[1]:
                if scallingY < pictures.shape[0]:
                    if scallingX >= 0:
                        if scallingY >= 0:
                            pictures[scallingY, scallingX] = currentFrame[y, x]
    return pictures


@njit(fastmath=True)
def rotationFrame(currentFrame, angle, center_X, center_Y):
    pictures = np.zeros(np.shape(currentFrame), np.uint8)

    # center_Y = int(pictures.shape[1] / 2 + (pictures.shape[1] / 2) * center_Y)
    # center_X = int(pictures.shape[0] / 2 + (pictures.shape[0] / 2) * center_X)

    for x in prange(pictures.shape[1]):
        for y in prange(pictures.shape[0]):
            rotatingX = int(cos(angle) * (x - center_X) - sin(angle) * (y - center_Y) + center_X)
            rotatingY = int(sin(angle) * (x - center_X) + cos(angle) * (y - center_Y) + center_X)
            if rotatingX < pictures.shape[1]:
                if rotatingY < pictures.shape[0]:
                    if rotatingX >= 0:
                        if rotatingY >= 0:
                            pictures[rotatingY, rotatingX] = currentFrame[y, x]
    return pictures

def reflectionFrame(currentFrame, verticalAxis, horizontalAxis):
    pictures = np.zeros(np.shape(currentFrame), np.uint8)

    for x in prange(pictures.shape[1]):
        for y in prange(pictures.shape[0]):
            newX = int(x * horizontalAxis + pictures.shape[0])
            newY = int(y * verticalAxis + pictures.shape[1])
            if newX < pictures.shape[1]:
                if newY < pictures.shape[0]:
                    if newX >= 0:
                        if newY >= 0:
                            pictures[newY, newX] = currentFrame[y, x]
    cv2.imshow("fs", pictures)
    return pictures

def reflectionMatrix(currentFrame, verticalAxis, horizontalAxis):
    plt.axis('off')
    rows, cols, dim = currentFrame.shape
    # if verticalAxis == -1 or horizontalAxis == -1:
    if horizontalAxis == -1:
        # transformation matrix for x-axis reflection
        M = np.float32([[1, 0, 0],
                        [0, -1, rows],
                        [0, 0, 1]])
        currentFrame = cv2.warpPerspective(currentFrame, M, (int(cols), int(rows)))
    if verticalAxis == -1:
    # transformation matrix for y-axis reflection
        M = np.float32([[-1, 0, cols],
                        [ 0, 1, 0   ],
                        [ 0, 0, 1   ]])
        currentFrame = cv2.warpPerspective(currentFrame, M, (int(cols), int(rows)))
    return currentFrame


