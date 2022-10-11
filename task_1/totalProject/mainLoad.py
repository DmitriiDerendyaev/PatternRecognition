import sys
import time

import taichi as ti
import userInterface
import functionFile as func

import numpy as np
import PySimpleGUI as sg
import os.path
import cv2
import random, string
from PIL import Image
import io
ti.init(arch=ti.cpu)


cannyThreshold = 30
cannyThresholdLinking = 30

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

#window = sg.Window("Demo", layout, size = (1000, 700))
sg.theme('DarkTeal11')
window = sg.Window("Demo", userInterface.layout, resizable=True).Finalize()
# window.Maximize()
cap = cv2.VideoCapture(0)

cap.set(3, 400)
cap.set(3, 400)


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

    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)

            cannyThreshold = int(values["-TH-"])
            cannyThresholdLinking = int(values["-TL-"])

            img = cv2.imread(filename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            window['-IMAGE-'].Update(data=func.cv2ToGUI(img))
        except:
            pass
    elif event == "-CannyF-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT_Converted-"].update(filename)

            cannyThreshold = int(values["-TH-"])
            cannyThresholdLinking = int(values["-TL-"])

            img = cv2.imread(filename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.Canny(img, cannyThreshold, cannyThresholdLinking)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(img))

            # destFile = randomword(7)
            # cv2.imwrite(r"D:\Eva\dacha\converted\Screenshot_8.png" + destFile + ".png", edges)
            # window["-IMAGE_OpenCV-"].update(r'D:\Eva\dacha\converted\Screenshot_8.png' + destFile + ".png")
        except:
            pass

    elif event == "-POROG_FILTER-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT_Converted-"].update(filename)

            current_frame = cv2.imread(filename)
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)

            delta = int(values["-color-"])

            merge_image = func.thresholdFilter(current_frame, delta)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(merge_image))

            # destFile = randomword(7)
            # cv2.imwrite(r"D:\Eva\dacha\converted\Screenshot_8.png" + destFile + ".png", merge_image)
            # window["-IMAGE_OpenCV-"].update(r'D:\Eva\dacha\converted\Screenshot_8.png' + destFile + ".png")
        except:
            pass

    elif event == "-WebCapture-":
        try:
            while True:
                event, values = window.read(timeout=10)

                if event == 'Exit' or values is None or event == "-WebCapture-":
                    sys.exit(0)

                ret, frame = cap.read()

                currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(currentFrame))

        except:
            pass
    elif event == "-BrowseVideo-":
        try:
            folder = values["-FOLDER-"]
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
            window["-FILE LIST-"].update(fnames)

            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT_Converted-"].update(filename)
            vid_capture = cv2.VideoCapture(filename)
            while True:

                event, values = window.read(timeout=10)

                if event == 'Exit' or values is None or event == "-StartStop-":
                    sys.exit(0)

                ret, frame = vid_capture.read()

                currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(currentFrame))
        except:
            pass
    elif event == "-StartStop-":
        try:
            while True:
                event, values = window.read(timeout=5)

                if event == 'Exit' or values is None or event == "-StartStop-":
                    sys.exit(0)

                ret, frame = vid_capture.read()

                currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(currentFrame))
        except:
            pass

    elif event == "-CannyVideo-":
        try:
            while True:
                event, values = window.read(timeout=5)

                if event == 'Exit' or values is None or event == "-StartStop-":
                    sys.exit(0)

                ret, frame = vid_capture.read()

                currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                currentFrame = cv2.Canny(currentFrame, cannyThreshold, cannyThresholdLinking)

                window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(currentFrame))
                #window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.thresholdFilter(filename)))
        except:
            pass
    elif event == "-SaveVideo-":
        try:
            video = cv2.VideoCapture(filename)


            if (video.isOpened() == False):
                print("Error reading video file")

            frame_width = int(video.get(3))
            frame_height = int(video.get(4))

            size = (frame_width, frame_height)

            result = cv2.VideoWriter('filename.avi',
                                     cv2.VideoWriter_fourcc(*'MJPG'),
                                     10, size)

            while (True):
                ret, frame = video.read()
                # frame = cv2.Canny(frame, cannyThreshold, cannyThresholdLinking)
                # frame = func.thresholdFilter(frame)
                if ret == True:
                    result.write(frame)

                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        break

                else:
                    break

            video.release()
            result.release()

        except:
            pass

window.close()