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


while True:
    event, values = window.read()

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
        imgDefault = img_before
        imgToPrint = img_before
        func.show_image(imgDefault, graph)


    if event == "-BrightnessValue-" or event == "-ContrastValue-" or event == "-BlurValue-":
        brightnessValue = values["-BrightnessValue-"]
        contrastValue = values["-ContrastValue-"]
        gaussianValue = int((values["-BlurValue-"] * 2) - 1)
        # img_before = cv2.addWeighted(imgDefault, contrastValue, imgDefault, 0, brightnessValue)

        img_before = func.BrightContrBlur(img_before, contrastValue, brightnessValue, gaussianValue)
        func.show_image(img_before, newGraph)

        # if event == "-BlurValue-":
        #     gaussianValue = int((values["-BlurValue-"]*2) - 1)
        #     print(gaussianValue)
        #     # imgToPrintBlur = cv2.GaussianBlur(img_before, (gaussianValue, gaussianValue), cv2.BORDER_DEFAULT)
        #     imgToPrintBlur = cv2.GaussianBlur(src=img_before, ksize=(gaussianValue, gaussianValue), sigmaX=0, sigmaY=0,
        #                                       borderType= cv2.BORDER_DEFAULT)
        #     func.show_image(imgToPrintBlur, newGraph)
        # else:
        #     func.show_image(img_before, newGraph)




    if values["-MonoChannel-"] or values["-RedChannel-"] or values["-BlueChannel-"] or values["-GreenChannel-"]:

        if values["-MonoChannel-"]:
            imgToPrint = cv2.cvtColor(img_before,cv2.COLOR_BGR2GRAY)
        if values["-RedChannel-"]:
            imgToPrint = func.splitFilter(img_before, 0)
        if values["-GreenChannel-"]:
            imgToPrint = func.splitFilter(img_before, 1)
        if values["-BlueChannel-"]:
            imgToPrint = func.splitFilter(img_before, 2)

        func.show_image(imgToPrint, newGraph)

        # if event == "-BlurValue-":
        #     gaussianValue = values["-BlurValue-"]
        #     imgToPrintBlur = cv2.GaussianBlur(imgToPrint, (gaussianValue, gaussianValue), cv2.BORDER_DEFAULT)
        #
        #     func.show_image(imgToPrintBlur, newGraph)
        # else:
        #     func.show_image(imgToPrint, newGraph)

window.close()