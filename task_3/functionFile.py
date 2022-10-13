from math import cos, sin

import cv2
from PIL import Image
import io
import numpy as np
from numba import njit, jit, prange
# import interface
# import PySimpleGUI as sg

def displayGraph(currentFrame, graph):
    scale = 350 / currentFrame.shape[1]
    dim = (round(currentFrame.shape[1] * scale), round(currentFrame.shape[0] * scale))

    correctFrame = cv2.resize(currentFrame, dim)

    frame_height, frame_width, channels = correctFrame.shape

    img_bytes = cv2.imencode('.png', correctFrame)[1].tobytes()

    graph.erase()
    huy = graph.draw_image(data=img_bytes, location=(450/2-frame_width/2, 450/2-frame_height/2))

    graph.send_figure_to_back(huy)

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
    huy = graph.draw_image(data=img_bytes, location=(450 / 2 - frame_width / 2, 450 / 2 - frame_height / 2))

    graph.send_figure_to_back(huy)

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
def rotationFrame(currentFrame, angle, center_X = 0, center_Y = 0):
    pictures = np.zeros(np.shape(currentFrame), np.uint8)

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


