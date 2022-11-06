import numpy as np

import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

window = sg.Window("Task 5", interface.layout, size=(1300, 700)).Finalize()
sg.theme('DarkTeal11')
graph = window["-GRAPH-"]
newGraph = window["-NEW_GRAPH-"]
start_point = end_point = prior_rect = None
isImg = False

while True:
    event, values = window.read(timeout=20)

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)

    if event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            img_before = cv2.imread(filename)
            isImg = True
            imgDefault = img_before
            imgToPrint = img_before
            imgToPrintTH = img_before
            func.show_image(imgDefault, graph)
        except:
            pass

    if values["-ThresholdBinaryText-"]:
        thresholdValue = int(values["-ThresholdValueText-"])
        imgToPrint = cv2.cvtColor(imgDefault, cv2.COLOR_BGR2GRAY)
        ret, imgToPrintTH = cv2.threshold(imgToPrint, thresholdValue, 255, cv2.THRESH_BINARY)
        imgToPrintTH = 255 - imgToPrintTH

        func.show_image(imgToPrintTH, newGraph)

    if values["-DilateText-"]:
        dilateValue = int(values["-DilateTextValue-"])
        print(dilateValue)
        kernel = np.ones((dilateValue, dilateValue), np.uint8)
        dilateImg = cv2.dilate(imgToPrintTH, kernel, iterations=1)
        func.show_image(dilateImg, newGraph)

    if values["-FindContours-"]:
        imgContours = imgDefault.copy()
        newRectContours = np.zeros(imgContours.shape)
        contours, hierarchy = cv2.findContours(dilateImg.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print((contours))
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)
        func.show_image(imgContours, newGraph)
        if values["-Find RECT-"]:
            contApprRec = []
            areaValue = int(values["-AreaValue-"])
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > areaValue:
                    rect = x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(imgContours, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    contApprRec.append(rect)
            func.show_image(imgContours, newGraph)

            # string = pytesseract.image_to_string(imgContours)
            # string = pytesseract.image_to_string(contApprRec[0])
            func.copyRect(imgContours, newRectContours, rect, rect)
            cv2.imshow("f", newRectContours)
            string = pytesseract.image_to_string(newRectContours)
            # печатаем
            print(string)


window.close()