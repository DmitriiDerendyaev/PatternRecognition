import cv2
from PIL import Image
import io
import numpy as np

import taichi as ti

ti.init(arch=ti.cpu)


def cv2ToGUI(currenFrame):
    scale = 300 / currenFrame.shape[1]
    dim = (round(currenFrame.shape[1] * scale), round(currenFrame.shape[0] * scale))

    correctFrame = cv2.resize(currenFrame, dim)

    img = Image.fromarray(correctFrame)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()

    return imgbytes


def splitFilter(currentFrame, choosenChannel, redImg=None):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)

    redChannel, greenChannel, blueChannel = cv2.split(currentFrame)
    print("splited channel")

    pictures = np.zeros(np.shape(currentFrame), np.uint8)

    if (choosenChannel == 0):
        pictures[:, :, choosenChannel] = redChannel
    elif (choosenChannel == 1):
        pictures[:, :, choosenChannel] = greenChannel
    elif (choosenChannel == 2):
        pictures[:, :, choosenChannel] = blueChannel

    return pictures


def makeBlack(currentFrame):
    return cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)


def makeBlackNumPy(currentFrame):
    print("in function")

    redChannel, greenChannel, blueChannel = cv2.split(currentFrame)

    totalImage = redChannel * 0.299 + greenChannel * 0.578 + blueChannel * 0.114

    return np.array(totalImage, np.uint8)


def changeContrast(currentFrame, contrastValue):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)

    (redChannel, greenChannel, blueChannel) = cv2.split(currentFrame)

    (redChannel) = cv2.multiply(redChannel, contrastValue)
    (greenChannel) = cv2.multiply(greenChannel, contrastValue)
    (blueChannel) = cv2.multiply(blueChannel, contrastValue)

    mergeFrame = cv2.merge([redChannel, greenChannel, blueChannel, ])
    return np.array(mergeFrame, np.uint8)


def changeBrightness(currentFrame, brightnessValue):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)

    (redChannel, greenChannel, blueChannel) = cv2.split(currentFrame)

    (redChannel) = cv2.add(redChannel, brightnessValue)
    (greenChannel) = cv2.add(greenChannel, brightnessValue)
    (blueChannel) = cv2.add(blueChannel, brightnessValue)

    mergeFrame = cv2.merge([redChannel, greenChannel, blueChannel])
    return np.array(mergeFrame, np.uint8)


def sepiaEffect(currentFrame, sepiaValue):
    # currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)

    (redChannel, greenChannel, blueChannel) = cv2.split(currentFrame)

    (redChannel) = redChannel * (0.393 + sepiaValue) + greenChannel * (0.769 + sepiaValue) + blueChannel * (
            0.189 + sepiaValue)
    (greenChannel) = redChannel * (0.349 + sepiaValue) + greenChannel * (0.686 + sepiaValue) + blueChannel * (
            0.168 + sepiaValue)
    (blueChannel) = redChannel * (0.272 + sepiaValue) + greenChannel * (0.534 + sepiaValue) + blueChannel * (
            0.131 + sepiaValue)

    mergeFrame = cv2.merge([redChannel, greenChannel, blueChannel, ])
    return np.array(mergeFrame, np.uint8)


def extensionImage(currentFrame):
    invertFrame = 255 - currentFrame

    return np.array(invertFrame, np.uint8)


def exclusionImage(firstFrame, secondFrame):
    exclusionFrame = firstFrame - secondFrame

    return np.array(exclusionFrame, np.uint8)


def intersectionImage(firstFrame, secondFrame):
    firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2RGB)
    secondFrame = cv2.cvtColor(secondFrame, cv2.COLOR_BGR2RGB)

    (redChannelF, greenChannelF, blueChannelF) = cv2.split(firstFrame)
    (redChannelS, greenChannelS, blueChannelS) = cv2.split(secondFrame)

    (redChannel) = np.maximum(redChannelF, redChannelS)
    (greenChannel) = np.maximum(greenChannelF, greenChannelS)
    (blueChannel) = np.maximum(blueChannelF, blueChannelS)

    mergeFrame = cv2.merge([redChannel, greenChannel, blueChannel, ])
    return np.array(mergeFrame, np.uint8)


def convertHSV(currentFrame, HueValue, SaturationValue, ValueValue):
    HSVframe = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2HSV)

    (HueChannel, SaturationChannel, ValueChannel) = cv2.split(HSVframe)
    print("splited channel")
    print(HueChannel)

    # (totalHue) = HueChannel + HueValue
    # (totalSaturation) = SaturationChannel + SaturationValue
    # (totalValue) = ValueChannel + ValueValue

    (totalHue) = cv2.add(HueChannel, HueValue)
    (totalSaturation) = cv2.add(SaturationChannel, SaturationValue)
    (totalValue) = cv2.add(ValueChannel, ValueValue)
    print(totalHue)

    print("after IF")

    mergeFrame = cv2.merge([totalHue, totalSaturation, totalValue])
    RGB = cv2.cvtColor(mergeFrame, cv2.COLOR_HSV2RGB)
    return np.array(RGB, np.uint8)


def medianBlurCV2(currentFrame, blurValue):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)
    totalFrame = cv2.medianBlur(currentFrame, 1 + blurValue * 2)

    return totalFrame


def medianBlurSelfDefault(currentFrame):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)

    totalFrame = cv2.copyMakeBorder(currentFrame, 1,1,1,1, cv2.BORDER_REPLICATE)
    (row, column) = totalFrame.shape
    bufferList = np.ones(dtype=np.uint8, shape=9)

    for currentRow in range(1, currentFrame.shape[0]):
        for currentColumn in range(1, currentFrame.shape[1]):
            bufferList[0] = totalFrame[currentRow - 1, currentColumn - 1]
            bufferList[1] = totalFrame[currentRow - 1, currentColumn]
            bufferList[2] = totalFrame[currentRow - 1, currentColumn + 1]
            bufferList[3] = totalFrame[currentRow, currentColumn - 1]
            bufferList[4] = totalFrame[currentRow, currentColumn]
            bufferList[5] = totalFrame[currentRow, currentColumn + 1]
            bufferList[6] = totalFrame[currentRow + 1, currentColumn - 1]
            bufferList[7] = totalFrame[currentRow + 1, currentColumn]
            bufferList[8] = totalFrame[currentRow + 1, currentColumn + 1]

            currentFrame[currentRow, currentColumn] = np.sort(bufferList)[4]

    return np.array(currentFrame, np.uint8)

bufferField = ti.field(ti.i32, shape=9)


@ti.func
def bubble_sort(array):
    for i in range(0, array.shape[0]-1):
        for j in range(array.shape[0]-1):
            if(array[j]>array[j+1]):
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
    return array

@ti.kernel
def calculatingMedian(currentFrame: ti.types.ndarray(), totalFrame: ti.types.ndarray(), row: int, column: int):
    for currentRow in range(1, row):
        for currentColumn in range(1, column):
            bufferField[0] = totalFrame[currentRow - 1, currentColumn - 1]
            bufferField[1] = totalFrame[currentRow - 1, currentColumn]
            bufferField[2] = totalFrame[currentRow - 1, currentColumn + 1]
            bufferField[3] = totalFrame[currentRow, currentColumn - 1]
            bufferField[4] = totalFrame[currentRow, currentColumn]
            bufferField[5] = totalFrame[currentRow, currentColumn + 1]
            bufferField[6] = totalFrame[currentRow + 1, currentColumn - 1]
            bufferField[7] = totalFrame[currentRow + 1, currentColumn]
            bufferField[8] = totalFrame[currentRow + 1, currentColumn + 1]

            currentFrame[currentRow, currentColumn] = bubble_sort(bufferField)[4]


def medianBlurSelf(currentFrame):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)

    totalFrame = cv2.copyMakeBorder(currentFrame, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
    (row, column) = totalFrame.shape
    # bufferList = np.ones(dtype=np.uint8, shape=9)

    calculatingMedian(currentFrame, totalFrame, row, column)

    return np.array(currentFrame, np.uint8)

def sharpenFilter(currentFrame, kernelMatrix):
    kernel = np.array(kernelMatrix)

    totalFrame = cv2.filter2D(currentFrame, -1, kernel)
    print(kernel)

    return totalFrame

@ti.kernel
def calculatingSharpen(currentFrame: ti.types.ndarray(), totalFrame: ti.types.ndarray(), row: int, column: int, kernelMatrix: ti.types.ndarray()):
    for currentRow in range(1, row):
        for currentColumn in range(1, column):
            bufferField[0] = (totalFrame[currentRow - 1, currentColumn - 1] * kernelMatrix[0])
            bufferField[1] = (totalFrame[currentRow - 1, currentColumn] * kernelMatrix[1])
            bufferField[2] = (totalFrame[currentRow - 1, currentColumn + 1] * kernelMatrix[2])
            bufferField[3] = (totalFrame[currentRow, currentColumn - 1] * kernelMatrix[3])
            bufferField[4] = (totalFrame[currentRow, currentColumn] * kernelMatrix[4])
            bufferField[5] = (totalFrame[currentRow, currentColumn + 1] * kernelMatrix[5])
            bufferField[6] = (totalFrame[currentRow + 1, currentColumn - 1] * kernelMatrix[6])
            bufferField[7] = (totalFrame[currentRow + 1, currentColumn] * kernelMatrix[7])
            bufferField[8] = (totalFrame[currentRow + 1, currentColumn + 1] * kernelMatrix[8])

            summaBuf = bufferField[0] + bufferField[1] + bufferField[2] + \
                    bufferField[3] + bufferField[4] + bufferField[5] + \
                    bufferField[6] + bufferField[7] + bufferField[8]

            summaKernel = kernelMatrix[0] + kernelMatrix[1] + kernelMatrix[2] + \
                    kernelMatrix[3] + kernelMatrix[4] + kernelMatrix[5] + \
                    kernelMatrix[6] + kernelMatrix[7] + kernelMatrix[8]


            currentFrame[currentRow, currentColumn] = summaBuf/summaKernel


def sharpenSelf(currentFrame, kerhelMatrix):
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)

    totalFrame = cv2.copyMakeBorder(currentFrame, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
    (row, column) = totalFrame.shape
    # bufferList = np.ones(dtype=np.uint8, shape=9)
    bufferKernel = np.array(kerhelMatrix, dtype=np.uint8)
    calculatingSharpen(currentFrame, totalFrame, row, column, bufferKernel)

    return np.array(currentFrame, np.uint8)

def additionImage(firstFrame, secondFrame):
    firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2RGB)
    secondFrame = cv2.cvtColor(secondFrame, cv2.COLOR_BGR2RGB)

    (redChannelF, greenChannelF, blueChannelF) = cv2.split(firstFrame)
    (redChannelS, greenChannelS, blueChannelS) = cv2.split(secondFrame)

    (redChannel) = cv2.add(redChannelF, redChannelS)
    (greenChannel) = cv2.add(greenChannelF, greenChannelS)
    (blueChannel) = cv2.add(blueChannelF, blueChannelS)

    mergeFrame = cv2.merge([redChannel, greenChannel, blueChannel, ])


    # addeitionFrame = cv2.addWeighted(firstFrame, 1, secondFrame, 1, 0.0)

    return np.array(mergeFrame, np.uint8)

def waterColor(currentFrame, addedFrame, Brightness, Contrast, Blur):
    brightnessedFrame = changeBrightness(currentFrame, Brightness)
    contrastedFrame = changeContrast(brightnessedFrame, Contrast)
    bluredFrame = medianBlurCV2(contrastedFrame, Blur)
    # addedFrame = medianBlurCV2(addedFrame, Blur)

    totalFrame = additionImage(bluredFrame, addedFrame)

    return np.array(totalFrame, np.uint8)

def intersectionImageCartoon(firstFrame, secondFrame):
    firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2RGB)

    (redChannelF, greenChannelF, blueChannelF) = cv2.split(firstFrame)

    (redChannel) = np.maximum(redChannelF, secondFrame)
    (greenChannel) = np.maximum(greenChannelF, secondFrame)
    (blueChannel) = np.maximum(blueChannelF, secondFrame)

    mergeFrame = cv2.merge([redChannel, greenChannel, blueChannel])
    return np.array(mergeFrame, np.uint8)

def cartoonFilter(currentFrame, blurValue, thresholdValue):
    blackFrame = makeBlack(currentFrame)
    totalFrame = cv2.medianBlur(blackFrame, 1 + blurValue * 2)
    ret, thresholdFrame = cv2.threshold(totalFrame, thresholdValue, 255, 0)
    # cv2.imshow("djfknvkdf", thresholdFrame)
    totalFrame = intersectionImageCartoon(currentFrame, thresholdFrame)
    # totalFrame = np.maximum(currentFrame, totalFrame)

    return totalFrame