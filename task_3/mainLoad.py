import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

window = sg.Window("Demo", interface.layout, size=(1300, 700))
sg.theme('DarkTeal11')
graph = window["-GRAPH-"]
newGraph = window["-NEW_GRAPH-"]
dragging = False
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
        img = cv2.imread(filename)
        print(img)

        func.displayGraph(img, graph)
    if values["-Scalling-"]:
        valueX = float(values["-ScallingX-"])
        valueY = float(values["-ScallingY-"])

        # func.scallingFrameCV2(img, valueX, valueY, newGraph)
        func.displayGraph(func.scallingFrame(img, valueX, valueY), newGraph)

    if values["-Shearing-"]:
        valueX = float(values["-ShearingX-"])
        valueY = float(values["-ShearingY-"])

        func.displayGraph(func.shearingFrame(img, valueX, valueY), newGraph)

    if values["-Rotation-"]:
        angle = float(values["-Angle-"])
        isGet = False

        if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
            x, y = values["-GRAPH-"]
            if not dragging:
                start_point = (x, y)
                dragging = True
                drag_figures = graph.get_figures_at_location((x, y))
                lastxy = x, y
            else:
                end_point = (x, y)
            if prior_rect:
                graph.delete_figure(prior_rect)
            delta_x, delta_y = x - lastxy[0], y - lastxy[1]
            lastxy = x, y
            if None not in (start_point, end_point):
                if values['-Rotation-']:
                    graph.draw_point((x, y), size=8)
                    print(x, y)
                    isGet = True
        if(isGet):
            func.displayGraph(func.rotationFrame(img, angle, x, y), newGraph)
        else:
            func.displayGraph(func.rotationFrame(img, angle, 225, 225), newGraph)




window.close()