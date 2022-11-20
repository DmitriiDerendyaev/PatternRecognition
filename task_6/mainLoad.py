import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

window = sg.Window("Task 4", interface.layout, size=(1300, 700)).Finalize()
sg.theme('DarkTeal11')
graph = window["-GRAPH-"]
newGraph = window["-NEW_GRAPH-"]
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
               and f.lower().endswith((".mp4"))
        ]
        window["-FILE LIST-"].update(fnames)

    if event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            video_captureVideo = cv2.VideoCapture(filename)
            img_before = cv2.imread(filename)
            func.show_image(img_before, graph)
        except:
            pass
    if event == "-SetCamera-":
        try:
            video_video_captureture = cv2.VideoCapture(0)
        except:
            pass
    if values["-CameraCapture-"]:
        try:
            ret, frame1 = video_capture.read()
            ret, frame2 = video_capture.read()

            diff = cv2.absdiff(frame1, frame2)

            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

            dilated = cv2.dilate(thresh, None,
                                 iterations=3)

            сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in сontours:
                (x, y, w, h) = cv2.boundingRect(
                    contour)

                print(cv2.contourArea(contour))

                if cv2.contourArea(contour) < 700:
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # cv2.drawContours(frame1, сontours, -1, (0, 255, 0), 2)

            func.show_image(frame2, graph)
            func.show_image(frame1, newGraph)


            # cv2.imshow("frame1", frame1)
            # frame1 = frame2  #
            # ret, frame2 = video_capture.read()  #

            if cv2.waitKey(40) == 27:
                break
        except:
            pass

    if event == "-SetVideo-":
        try:
            video_capture = cv2.VideoCapture(filename)
        except:
            pass
    if values["-VideoCapture-"]:
        try:
            ret, frame1 = video_capture.read()
            ret, frame2 = video_capture.read()

            diff = cv2.absdiff(frame1, frame2)

            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

            dilated = cv2.dilate(thresh, None,
                                 iterations=3)

            сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in сontours:
                (x, y, w, h) = cv2.boundingRect(
                    contour)

                print(cv2.contourArea(contour))

                if cv2.contourArea(contour) < 700:
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # cv2.drawContours(frame1, сontours, -1, (0, 255, 0), 2)

            func.show_image(frame2, graph)
            func.show_image(frame1, newGraph)


            # cv2.imshow("frame1", frame1)
            # frame1 = frame2  #
            # ret, frame2 = video_capture.read()  #

            if cv2.waitKey(40) == 27:
                break
        except:
            pass