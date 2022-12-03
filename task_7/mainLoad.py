import numpy as np

import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

window = sg.Window("Task 7", interface.layout, size=(1300, 700)).Finalize()
sg.theme('DarkTeal11')
graph = window["-GRAPH-"]
newGraph = window["-NEW_GRAPH-"]
feature_points = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)
parameters = dict(winSize=(15, 15),
                  maxLevel=2,
                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0,255,(100,3))




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

    if values["-FIRST_IMG-"]:
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
    if values["-SECOND_IMG-"]:
        if event == "-FILE LIST-":
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
                img_second = cv2.imread(filename)
                func.show_image(img_second, newGraph)
            except:
                pass
    if event == "-PointsGFTT-":
        gfft = cv2.GFTTDetector_create()

        key_first = gfft.detect(img_before, None)

        img2 = img_before.copy()
        img2 = cv2.drawKeypoints(img_before, key_first, img2, color=(0, 255, 0))


        img_beforeGrey = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
        img_secondGrey = cv2.cvtColor(img_second, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(img_before)

        points = cv2.goodFeaturesToTrack(img_beforeGrey, mask=None, **feature_points)
        respoints, status, errors = cv2.calcOpticalFlowPyrLK(img_beforeGrey,
                                                             img_secondGrey,
                                                             points, None,
                                                             **parameters)
        good_new = respoints[status == 1]
        good_old = points[status == 1]

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a,b = new.ravel()
            aa = int(a)
            bb = int(b)
            img_before = cv2.circle(img_before, (aa, bb), 5, color[i].tolist(), -1)

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a,b = new.ravel()
            aa = int(a)
            bb = int(b)
            img_second = cv2.circle(img_second, (aa, bb), 5, color[i].tolist(), -1)

        matrixMy, status = cv2.findHomography(points, respoints)

        homo_image = cv2.warpPerspective(img_second, matrixMy, (img_second.shape[1], img_second.shape[0]))

        func.show_image(img_before, graph)
        func.show_image(homo_image, newGraph)
        print(respoints.shape)


    if event == "-PointsBRISK-":

        img1, img2 = img_before, img_second

        gray_pic1, gray_pic2 = func.convert_to_grayscale(img1, img2)

        key_pt1, descrip1, key_pt2, descrip2 = func.detector(gray_pic1, gray_pic2)

        number_of_matches = func.BF_FeatureMatcher(descrip1, descrip2)
        tot_feature_matches = len(number_of_matches)

        output = func.display_output(gray_pic1, key_pt1, gray_pic2, key_pt2, number_of_matches)
        cv2.imshow("fff", output)
        # func.show_image(output,newGraph)

