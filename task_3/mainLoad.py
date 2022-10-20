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
        img = img_before
        func.show_image(img, graph)
        first_mas = np.array([[0, 0]])
        second_mas = np.array([[0, 0]])
    if values["-Scalling-"]:
        func.displayGraph(img_before, graph)
        valueX = float(values["-ScallingX-"])
        valueY = float(values["-ScallingY-"])

        # func.scallingFrameCV2(img, valueX, valueY, newGraph)
        if values["-Bilinear-"] == True:
            func.displayGraph(func.bilinear_scalling(img, valueX, valueY), newGraph)
        else:
            func.displayGraph(func.scallingFrame(img, valueX, valueY), newGraph)


    if values["-Shearing-"]:
        func.displayGraph(img_before, graph)
        valueX = float(values["-ShearingX-"])
        valueY = float(values["-ShearingY-"])

        func.displayGraph(func.shearingFrame(img, valueX, valueY), newGraph)
        func.show_image(func.shearingFrame(img, valueX, valueY), newGraph)

    if values["-Rotation-"]:
        func.show_image(img_before, graph)
        if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
            x, y = values["-GRAPH-"]
            coordinatesXY = str(x), str(y)
            x_img = int(x - (450 - (func.find_size(img_before)).shape[1])/2)
            y_img = int(y - (450 - (func.find_size(img_before)).shape[0])/2)

            y_img = int(y_img*(img_before.shape[0]/func.find_size(img_before).shape[0]))
            x_img = int(x_img*(img_before.shape[1]/func.find_size(img_before).shape[1]))

            graph.draw_circle(values['-GRAPH-'], 5, fill_color='red', line_color='black')


        if event == "-Angle-":
            if values["-Bilinear-"]:
                func.show_image(func.custom_rotation_bilinear(img_before, values["-Angle-"], y_img, x_img), newGraph)
                graph.draw_circle(values['-GRAPH-'], 5, fill_color='red', line_color='black')
            else:
                func.show_image(func.rotationFrame(img_before, values["-Angle-"], x_img, y_img), newGraph)
                graph.draw_circle(values['-GRAPH-'], 5, fill_color='red', line_color='black')

    if values["-Reflection-"]:
        func.show_image(img_before, graph)
        vertical = int(values["-Vertical-"])

        horizontal = int(values["-Horizontal-"])

        func.show_image(func.reflectionMatrix(img_before, vertical, horizontal), newGraph)
        # func.reflectionMatrix(img_before, vertical, horizontal)


    if values["-Projection-"]:
        if event == "Erase item-Origin":
            first_mas = np.array([[0, 0]])
            graph.erase()
            func.show_image(img_before, graph)
        if event == "Erase item-CV2":
            second_mas = np.array([[0, 0]])
            graph.erase()
            func.show_image(img_before, graph)

        if event == '-GRAPH-':
            if first_mas.shape[0] < 5:
                x, y = values["-GRAPH-"]
                coordinatesXY = str(x), str(y)
                x_img = int(x - (450 - (func.find_size(img_before)).shape[1]) / 2)
                y_img = int(y - (450 - (func.find_size(img_before)).shape[0]) / 2)

                y_img = int(y_img * (img_before.shape[0] / func.find_size(img_before).shape[0]))
                x_img = int(x_img * (img_before.shape[1] / func.find_size(img_before).shape[1]))

                graph.draw_circle(values['-GRAPH-'], 5, fill_color='red', line_color='black')
                first_mas = np.append(first_mas, [[x_img, y_img]], axis=0)
                graph.draw_circle(values['-GRAPH-'], 5, fill_color='red', line_color='black')
            if first_mas.shape[0] >= 4:
                print(first_mas)

        if event == "-HOMO-":
            print("HOMO")
            first_mas = np.delete(first_mas, 0, 0)
            second_mas = np.delete(second_mas, 0, 0)

            first_mas = np.float32(first_mas)
            second_mas = np.float32([
                [0, 0],
                [0, 450 - 1.0],
                [450 - 1.0, 450 - 1.0],
                [450 - 1.0, 0],
            ])

            homo = cv2.getPerspectiveTransform(first_mas, second_mas)

            homo_image = cv2.warpPerspective(img_before, homo, (img_before.shape[0], img_before.shape[1]))
            # cv2.imshow("srtg", homo_image)
            func.show_image(homo_image, newGraph)





window.close()