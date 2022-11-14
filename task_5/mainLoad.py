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
x_img = 0
y_img = 0
string = ""
video_capture = cv2.VideoCapture(0)

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

    if event == "-FOLDER_VIDEO-":
        folder = values["-FOLDER_VIDEO-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
               and f.lower().endswith((".mp4"))
        ]
        window["-FILE LIST VIDEO-"].update(fnames)

    if event == "-FILE LIST VIDEO-":
        try:
            filename = os.path.join(
                values["-FOLDER_VIDEO-"], values["-FILE LIST VIDEO-"][0]
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
        kernel = np.ones((dilateValue, dilateValue), np.uint8)
        dilateImg = cv2.dilate(imgToPrintTH, kernel, iterations=1)
        func.show_image(dilateImg, newGraph)

    if values["-FindContours-"]:
        imgContours = imgDefault.copy()
        newRectContours = np.zeros(imgContours.shape)
        contours, hierarchy = cv2.findContours(dilateImg.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)
        func.show_image(imgContours, newGraph)
        if values["-Find RECT-"]:
            contApprRec = []
            areaValue = int(values["-AreaValue-"])
            if event == "-NEW_GRAPH-":  # if there's a "Graph" event, then it's a mouse
                x, y = values["-NEW_GRAPH-"]
                coordinatesXY = str(x), str(y)
                x_img = int(x - (450 - (func.find_size(img_before)).shape[1]) / 2)
                y_img = int(y - (450 - (func.find_size(img_before)).shape[0]) / 2)

                y_img = int(y_img * (img_before.shape[0] / func.find_size(img_before).shape[0]))
                x_img = int(x_img * (img_before.shape[1] / func.find_size(img_before).shape[1]))
                print(y_img, x_img)
                newGraph.draw_circle(values['-NEW_GRAPH-'], 5, fill_color='red', line_color='black')

                for contour in contours:
                    area = cv2.contourArea(contour)
                    rect = x, y, w, h = cv2.boundingRect(contour)
                    if x_img > x and y_img > y and x_img < x+w and y_img < y+h:
                        string = pytesseract.image_to_string(imgContours[y:y+h, x:x+w].copy())
                    cv2.rectangle(imgContours, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    contApprRec.append(rect)
            window['-OUTPUT-'].update(string)
            newGraph.draw_circle(values['-NEW_GRAPH-'], 5, fill_color='red', line_color='black')
            func.show_image(imgContours, newGraph)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if event == "-GetCamera-":
        video_capture = cv2.VideoCapture(0)
    if values["-ShowCamera-"]:

        _, frame = video_capture.read()

        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(image=grayscale_image, scaleFactor=1.3, minNeighbors=4)
        func.draw_found_faces(detected_faces, frame, (0, 0, 255))
        func.show_image(frame, newGraph)

        if cv2.waitKey(1) == 27:
            break
    if event == "-GetVideo-":
        video_capture = cv2.VideoCapture(filename)
    if values["-ShowVideo-"]:
        _, frame = video_capture.read()

        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(image=grayscale_image, scaleFactor=1.3, minNeighbors=4)
        func.draw_found_faces(detected_faces, frame, (0, 0, 255))
        func.show_image(frame, newGraph)

        if cv2.waitKey(1) == 27:
            break

window.close()