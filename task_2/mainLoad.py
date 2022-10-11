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
# window = sg.Window("Demo", interface.layout, resizable=True).Finalize()
# window.Maximize()


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
    if values["-RedChannel-"]:
        try:
            print("in red")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            newFrame = func.splitFilter(img, 0)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(newFrame))
        except:
            pass
    if values["-GreenChannel-"]:
        try:
            print("in green")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            newFrame = func.splitFilter(img, 1)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(newFrame))
        except:
            pass
    if values["-BlueChannel-"]:
        try:
            print("in blue")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            newFrame = func.splitFilter(img, 2)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(newFrame))
        except:
            pass
    if values["-Black-"]:
        # try:
        print("in black")
        window["-TOUT_Converted-"].update(filename)
        img = cv2.imread(filename)

        # window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.makeBlack(img)))
        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.makeBlackNumPy(img)))
        # except:
        #     pass
    if values["-Contrast-"]:
        # try:
        if (values["-Contrast-"]):
            print("in filter")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            contrastValue = float(values["-ContrastValue-"])
            print(contrastValue)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.changeContrast(img, contrastValue)))
        # except:
        #     pass
    if values["-Brightness-"]:
        # try:
        if (values["-Brightness-"]):
            print("in filter")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            brightnessValue = int(values["-BrightnessValue-"])
            print(brightnessValue)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.changeBrightness(img, brightnessValue)))
        # except:
        #     pass
    if values["-Sepia-"]:
        # try:
        if (values["-SepiaValue-"]):
            print("in filter")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            SepiaValue = float(values["-SepiaValue-"])
            print(SepiaValue)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.sepiaEffect(img, SepiaValue)))
        # except:
        #     pass
    if values["-Sepia-"]:
        # try:
        if (values["-SepiaValue-"]):
            print("in filter")
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            SepiaValue = float(values["-SepiaValue-"])
            print(SepiaValue)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.sepiaEffect(img, SepiaValue)))
        # except:
        #     pass
    if event == "-AddFirst-":
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT-"].update(filename)
        first_image = cv2.imread(filename)
    if event == "-AddSecond-":
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT-"].update(filename)
        second_image = cv2.imread(filename)

    if values["-Extension-"]:
        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.extensionImage(first_image)))

    if values["-Exclusion-"]:
        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.exclusionImage(first_image, second_image)))

    if values["-Intersection-"]:
        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.intersectionImage(first_image, second_image)))

    if values["-HSV-"]:
        print("in filter")
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT_Converted-"].update(filename)
        img = cv2.imread(filename)

        HueValue = int(values["-HueValue-"])
        SaturationValue = int(values["-SaturationValue-"])
        ValueValue = int(values["-ValueValue-"])
        print(HueValue)

        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.convertHSV(img, HueValue, SaturationValue, ValueValue)))

    if values["-Blur-"]:
        # try:
        if (values["-BlurValue-"]):
            print("in filter")
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            BlurValue = int(values["-BlurValue-"])
            print(BlurValue)

            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.medianBlurCV2(img, BlurValue)))
        # except:
        #     pass

    if values["-BlurMatrix-"]:
        # try:
        print("in filter")
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT_Converted-"].update(filename)
        img = cv2.imread(filename)

        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.medianBlurSelf(img)))
        # except:
        #     pass

    if values["-Sharpen-"]:
        # try:
        print("in filter")
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT_Converted-"].update(filename)
        img = cv2.imread(filename)

        matrix = int(values["-00-"]), int(values["-01-"]), int(values["-02-"]), \
                                int(values["-10-"]), int(values["-11-"]), int(values["-12-"]), \
                                int(values["-20-"]), int(values["-21-"]), int(values["-22-"])


        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.sharpenFilter(img, matrix)))
        # except:
        #     pass
    if values["-SharpenMatrix-"]:
            # try:
            print("in filter")
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT_Converted-"].update(filename)
            img = cv2.imread(filename)

            matrix = int(values["-00-"]), int(values["-01-"]), int(values["-02-"]), \
                                    int(values["-10-"]), int(values["-11-"]), int(values["-12-"]), \
                                    int(values["-20-"]), int(values["-21-"]), int(values["-22-"])


            window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.sharpenSelf(img, matrix)))
            # except:
            #     pass
    if event == "-AddImage-":
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT-"].update(filename)
        addedImage = cv2.imread(filename)
    if event == "-AddMask-":
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT-"].update(filename)
        maskImage = cv2.imread(filename)
    if values["-CartoonFilter-"]:
        img = cv2.imread(filename)
        BlurValueCartoon = int(values["-BlurValueCartoon-"])
        print(BlurValueCartoon)
        ThresholdValueCartoon = int(values["-ThresholdValueCartoon-"])
        print(ThresholdValueCartoon)

        window['-IMAGE_OpenCV-'].Update(data=func.cv2ToGUI(func.cartoonFilter(img, BlurValueCartoon, ThresholdValueCartoon)))

window.close()
