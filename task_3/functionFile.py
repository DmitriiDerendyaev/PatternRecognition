from math import cos, sin, floor

import cv2

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

def find_size(image):
    if image.shape[1] > 450:
        scale = 450 / image.shape[1]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    if image.shape[0] > 450:
        scale = 450 / image.shape[0]
        dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
        image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    if image.shape[0] < 450 and image.shape[1] < 450:
        if image.shape[0] > image.shape[1]:
            scale = 450 / image.shape[0]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

        else:
            scale = 450 / image.shape[1]
            dim = (round(image.shape[1] * scale), round(image.shape[0] * scale))
            image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    return image


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
    img = graph.draw_image(data=img_bytes, location=(450 / 2 - frame_width / 2, 450 / 2 - frame_height / 2))

    graph.send_figure_to_back(img)

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

    # resPictures = np.zeros(np.shape(pictures), np.uint8)
    # for x in prange(pictures.shape[1]):
    #     for y in prange(pictures.shape[0]):
    #         floorX = floor(x)
    #         floorY = floor(y)
    #         ratioX = x - floorX
    #         ratioY = y - floorY
    #         invertsXratio = 1 - ratioX
    #         invertsYratio = 1 - ratioY
    #         resPictures[scallingY, scallingX] = (pictures[x, y] * invertsYratio + pictures[x + 1, y] * ratioX) * invertsYratio + (pictures[x, y + 1] * invertsXratio + pictures[x + 1, y + 1] * ratioX) * ratioY


    return pictures


@njit(fastmath=True, parallel=True)
def bilinear_scalling(image, sX, sY):

    new_image = np.zeros(image.shape, np.uint8)
    for x in prange(image.shape[1]):
        for y in prange(image.shape[0]):
            new_x = int(x*sX)
            if new_x >= new_image.shape[1]:
                continue
            if x < image.shape[1]-1:
                new_next_x = int((x+1)*sX)
                if new_next_x > image.shape[1]:
                    new_next_x = image.shape[1]-1
                for i in range(new_x, new_next_x):
                    omega = (i-new_x)/(new_next_x-new_x)
                    new_value = image[y, x] * (1 - omega) + image[y, x+1] * omega
                    if i < image.shape[1]:
                        new_image[y, i] = new_value

    image = new_image
    new_image = np.zeros(image.shape, np.uint8)
    for x in prange(image.shape[1]):
        for y in prange(image.shape[0]):
            new_y = int(y*sY)
            if new_y >= new_image.shape[0]:
                continue
            if y < image.shape[0]-1:
                new_next_y = int((y+1)*sY)
                if new_next_y > image.shape[0]:
                    continue
                for i in range(new_y, new_next_y):
                    omega = (i-new_y)/(new_next_y-new_y)
                    new_value = image[y, x] * (1 - omega) + image[y+1, x] * omega
                    if i < image.shape[0]:
                        new_image[i, x] = new_value
    return new_image

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
            rotatingY = int(sin(angle) * (x - center_X) + cos(angle) * (y - center_Y) + center_Y)
            if rotatingX < pictures.shape[1]:
                if rotatingY < pictures.shape[0]:
                    if rotatingX >= 0:
                        if rotatingY >= 0:
                            pictures[rotatingY, rotatingX] = currentFrame[y, x]
    return pictures

@njit(fastmath=True)
def custom_rotation_bilinear(image, angle, y_center, x_center):
    new_image = np.zeros(image.shape, np.uint8)
    # y_center = int(image.shape[0] / 2 + (image.shape[0] / 2) * y_center)
    # x_center = int(image.shape[1] / 2 + (image.shape[1] / 2) * x_center)
    for x in prange(image.shape[1]):
        for y in prange(image.shape[0]):
            new_x = int(cos(angle) * (x - x_center) - sin(angle) * (y - y_center) + x_center)
            new_y = int(sin(angle) * (x - x_center) + cos(angle) * (y - y_center) + y_center)
            if new_x < image.shape[1]:
                if new_y < image.shape[0]:
                    if new_x >= 0:
                        if new_y >= 0:
                            new_image[new_y, new_x] = image[y, x]

    for y in prange(image.shape[0]):
        flag = True
        for x in prange(image.shape[1] - 1):
            if new_image[y, x, 0] == 0 and new_image[y, x, 1] == 0 and new_image[y, x, 2] == 0:
                if flag:
                    continue
                next_x = x
                while new_image[y, next_x, 0] == 0 and new_image[y, next_x, 1] == 0 and new_image[
                    y, next_x, 2] == 0:
                    next_x += 1
                    if next_x >= new_image.shape[1] - 1:
                        break
                    if next_x - x >= 10:
                        break
                for i in range(x, next_x):

                    omega = (i - x) / (next_x - x)
                    new_value = new_image[y, x - 1] * (1 - omega) + new_image[y, next_x] * omega
                    if i < image.shape[1]:
                        new_image[y, i] = new_value
            else:
                flag = False
    return new_image

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


