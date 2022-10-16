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
    if values["-Scalling-"]:
        func.displayGraph(img_before, graph)
        valueX = float(values["-ScallingX-"])
        valueY = float(values["-ScallingY-"])

        # func.scallingFrameCV2(img, valueX, valueY, newGraph)
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

            func.show_image(func.rotationFrame(img_before, values["-Angle-"], x_img, y_img), newGraph)
            graph.draw_circle(values['-GRAPH-'], 5, fill_color='red', line_color='black')

    if values["-Reflection-"]:
        func.show_image(img_before, graph)
        vertical = int(values["-Vertical-"])

        horizontal = int(values["-Horizontal-"])

        func.show_image(func.reflectionMatrix(img_before, vertical, horizontal), newGraph)
        # func.reflectionMatrix(img_before, vertical, horizontal)




window.close()