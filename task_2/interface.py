import PySimpleGUI as sg

sg.theme('DarkTeal11')

first_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(15,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(35,15),
            key="-FILE LIST-"
        )
    ],
    [
        sg.Radio("Red", "RADIO1", enable_events=True, default=False, key="-RedChannel-"),
        sg.Radio("Green", "RADIO1", enable_events=True, default=False, key="-GreenChannel-"),
        sg.Radio("Blue", "RADIO1", enable_events=True, default=False, key="-BlueChannel-"),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Radio("Brightness", "RADIO1", enable_events=True, default=False, key="-Brightness-"),
        # sg.Push(background_color = None),
        sg.Radio("Black", "RADIO1", enable_events=True, default=False, key="-Black-"),
        sg.Radio("Contrast", "RADIO1", enable_events=True, default=False, key="-Contrast-"),
    ],
    [
        sg.Slider(range=(0,100), enable_events=True, key="-BrightnessValue-", default_value=1, resolution=.1, size=(15,10), orientation='horizontal'),
        sg.Slider(range=(0.5,2), enable_events=True, key="-ContrastValue-", default_value=1, resolution=0.05,
                  size=(15,10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Radio("Sepia", "RADIO1", enable_events=True, default=False, key="-Sepia-"),
        sg.Slider(range=(-0.2, 0.1), enable_events=True, key="-SepiaValue-", default_value=0, resolution=0.001, size=(15,10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Button("Add first image", key="-AddFirst-"),
        sg.Button("Add second image", key="-AddSecond-")

    ],
    [
        sg.Radio("Extension", "RADIO1", enable_events=True, default=False, key="-Extension-"),
        sg.Radio("Exclusion", "RADIO1", enable_events=True, default=False, key="-Exclusion-"),
        sg.Radio("Intersection", "RADIO1", enable_events=True, default=False, key="-Intersection-"),
    ],
    [sg.HorizontalSeparator()],
    [
        # sg.Radio("Hue", "RADIO1", enable_events=True, default=False, key="-Hue-"),
        sg.Push(background_color=None),
        sg.Slider(range=(-255, 255), enable_events=True, key="-HueValue-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [
        sg.Radio("HSV", "RADIO1", enable_events=True, default=False, key="-HSV-"),
        sg.Push(background_color=None),
        sg.Slider(range=(-255, 255), enable_events=True, key="-SaturationValue-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [
        # sg.Radio("Value", "RADIO1", enable_events=True, default=False, key="-Value-"),
        sg.Push(background_color=None),
        sg.Slider(range=(-255, 255), enable_events=True, key="-ValueValue-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Radio("Blur", "RADIO1", enable_events=True, default=False, key="-Blur-"),
        sg.Slider(range=(0, 50), enable_events=True, key="-BlurValue-", default_value=0, resolution=0.5, size=(15,10), orientation='horizontal'),
    ],
    [sg.Radio("Blur Matrix", "RADIO1", enable_events=True, default=False, key="-BlurMatrix-"),],
    [sg.HorizontalSeparator()],
    [
        sg.Radio("Sharpen", "RADIO1", enable_events=True, default=False, key="-Sharpen-"),
        sg.Radio("SharpenMatrix", "RADIO1", enable_events=True, default=False, key="-SharpenMatrix-"),
    ],
    [
        sg.InputText(size=(3,1), key="-00-", default_text=-1), sg.InputText(size=(3,1), key="-01-", default_text=-1), sg.InputText(size=(3,1), key="-02-", default_text=-1)
    ],
    [
        sg.InputText(size=(3,1), key="-10-", default_text=-1), sg.InputText(size=(3,1), key="-11-", default_text=9), sg.InputText(size=(3,1), key="-12-", default_text=-1)
    ],
    [
        sg.InputText(size=(3,1), key="-20-", default_text=-1), sg.InputText(size=(3,1), key="-21-", default_text=-1), sg.InputText(size=(3,1), key="-22-", default_text=-1)
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Push(background_color=None),
        sg.Text("Brightness"),
        sg.Push(background_color=None),
        sg.Text("Contrast"),
        sg.Push(background_color=None),
        sg.Text("Blur"),
        sg.Push(background_color=None),
    ],
    [
        sg.Slider(range=(-100, 100), enable_events=True, key="-BrightnessValueWater-", default_value=1, resolution=.1,
                  size=(10, 10), orientation='horizontal'),
        sg.Slider(range=(0.5, 2), enable_events=True, key="-ContrastValueWater-", default_value=1, resolution=0.05,
                  size=(10, 10), orientation='horizontal'),
        sg.Slider(range=(0, 50), enable_events=True, key="-BlurValueWater-", default_value=0, resolution=0.5, size=(10,10),
                  orientation='horizontal'),
    ],
    [
        sg.Button("Add Image", key="-AddImage-"),
        sg.Button("Add Mask", key="-AddMask-"),
        sg.Radio("Watercolor", "RADIO1", enable_events=True, default=False, key="-WaterColorFilter-"),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Push(background_color=None),
        sg.Text("Contrast"),
        sg.Text("Blur"),
        sg.Push(background_color=None),
    ],
    [
        sg.Slider(range=(0, 50), enable_events=True, key="-BlurValueCartoon-", default_value=1, resolution=1,
                  size=(10, 10), orientation='horizontal'),
        sg.Slider(range=(0, 254), enable_events=True, key="-ThresholdValueCartoon-", default_value=127, resolution=1, size=(10,10),
                  orientation='horizontal'),
    ],
    [
        sg.Radio("Cartoon filter", "RADIO1", enable_events=True, default=False, key="-CartoonFilter-"),
    ]
    ]



image_original_column = [
    [sg.Text("Choose an image from list:")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

image_OpenCV_column = [
    [sg.Text("Result of work OpenCV:")],
    [sg.Text(size=(40,1),key="-TOUT_Converted-")],
    [sg.Image(key="-IMAGE_OpenCV-")],
]

layout = [
    [
        sg.Column(first_list_column,element_justification='c', size=(300, 700), scrollable=True),
        sg.VSeparator(),
        sg.Column(image_original_column),
        sg.VSeparator(),
        sg.Column(image_OpenCV_column),
    ]
]
