import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

window = sg.Window("Task 7", interface.layout, size=(1300, 700)).Finalize()
sg.theme('DarkTeal11')
graph = window["-GRAPH-"]
newGraph = window["-NEW_GRAPH-"]

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
               and f.lower().endswith((".png"))
        ]
        window["-FILE LIST-"].update(fnames)

    if values["FIRST_IMG"]:
        if event == "-FILE LIST-":
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
                img_before = cv2.imread(filename)
                func.show_image(img_before, graph)
            except:
                pass
    if event == "-PointsGFTT-":
        gfft = cv2.GFTTDetector_create()

        key = gfft.detect(img_before, None)

        img2 = img_before.copy()
        img2 = cv2.drawKeypoints(img_before, key, img2, color=(0, 255, 0))

        func.show_image(img2, newGraph)
        print(key)

        cv2.calcOpticalFlowPyrLK()


    if event == "-PointsBRISK-":
        brisk = cv2.BRISK_create()

        keypoints = brisk.detect(img_before, None)

        img2 = img_before.copy()
        img2 = cv2.drawKeypoints(img_before, keypoints, img2, color=(0, 255, 0))

        func.show_image(img2, newGraph)