import numpy as np

import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

window = sg.Window("Demo", interface.layout, size=(1300, 700)).Finalize()
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

    if event != "--TIMEOUT--" and event != "-FOLDER-" and isImg:
        preImage = func.preImage(event, values, img_before)
        func.show_image(preImage, newGraph)

    if values["-FindContours-"]:
        imgContours = imgDefault.copy()
        contours, hierarchy = cv2.findContours(preImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        cv2.drawContours(imgContours, contours, -1, (0,255,0), 3)
        func.show_image(imgContours, newGraph)

    # if values["-ApproximationContours-"]:
    #     approximationValue = values["-ApproximationValue-"]
    #     countAppr = []
    #     for count in contours:
    #         epsilon = (approximationValue / 100) * cv2.arcLength(count, True)
    #         print(epsilon)
    #         # count = cv2.approxPolyDP(count, epsilon, True)
    #         countAppr.append(cv2.approxPolyDP(count, epsilon, True))
    #     cv2.drawContours(imgContours, countAppr, -1, (0, 0, 255), 3)
    #     func.show_image(imgContours, newGraph)

    if values["-ApproximationContours-"]:
        approximationValue = values["-ApproximationValue-"]
        countAppr = []
        for count in contours:
            epsilon = (approximationValue / 100) * cv2.arcLength(count, True)
            print(epsilon)
            # count = cv2.approxPolyDP(count, epsilon, True)
            countAppr.append(cv2.approxPolyDP(count, epsilon, True))
        cv2.drawContours(imgContours, countAppr, -1, (0, 0, 255), 3)
        func.show_image(imgContours, newGraph)


window.close()