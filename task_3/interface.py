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
            values=[], enable_events=True, size=(35, 15),
            key="-FILE LIST-"
        )
    ],
    ]

image_original_column = [
    [sg.Text("Choose an image from list:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

image_OpenCV_column = [
    [sg.Text("Result of work OpenCV:")],
    [sg.Text(size=(40, 1), key="-TOUT_Converted-")],
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