import interface
import functionFile as func

import PySimpleGUI as sg
import os.path
import cv2

#
# import taichi as ti
#
# ti.init(arch=ti.cpu)

window = sg.Window("Demo", interface.layout, size=(1000, 700))
sg.theme('DarkTeal11')

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
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            img = cv2.imread(filename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # first_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # second_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            window['-IMAGE-'].Update(data=func.cv2ToGUI(img))
        except:
            pass