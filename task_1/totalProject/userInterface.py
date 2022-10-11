import PySimpleGUI as sg

sg.theme('DarkTeal11')

first_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20),
            key="-FILE LIST-"
        )
    ],
    [
        sg.Button("Show Photo", key="-PHOTO-"),
        sg.Button("Canny Mask", key="-CannyF-"),
        sg.Button("Color Filter", key="-POROG_FILTER-"),
    ],
    [
        sg.Text("cannyThreshold: ")
    ],
    [
        sg.Slider(range=(0,600),key="-TH-", default_value=100, resolution=.1, size=(40,15), orientation='horizontal')
    ],
    [
        sg.Text("cannyThresholdLinking: ")
    ],
    [
        sg.Slider(range=(0,600),key="-TL-", default_value=100, resolution=.1, size=(40,15), orientation='horizontal')
    ],
    [
        sg.Text("Color: ")
    ],
    [
        sg.Slider(range=(-50,50),key="-color-", default_value=0, resolution=.1, size=(40,15), orientation='horizontal')
    ],
    [
        sg.Button("WebCamera", key="-WebCapture-"),
    ],
    [
        sg.Button("Browse Video", key="-BrowseVideo-"),
        sg.Button("Start/Stop", key="-StartStop-"),
        sg.Button("Activate Canny", key="-CannyVideo-"),
    ],
    [
        sg.Button("Save Video", key="-SaveVideo-"),
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
        sg.Column(first_list_column),
        sg.VSeparator(),
        sg.Column(image_original_column),
        sg.VSeparator(),
        sg.Column(image_OpenCV_column),
    ]
]
