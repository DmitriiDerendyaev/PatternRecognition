import PySimpleGUI as sg

sg.theme('DarkTeal11')

first_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(15, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(35, 15),
            key="-FILE LIST-"
        )
    ],
    [
        sg.Radio("Grey", "RADIO1", enable_events=True, default=False, key="-MonoChannel-"),
        sg.Radio("Red", "RADIO1", enable_events=True, default=False, key="-RedChannel-"),
        sg.Radio("Green", "RADIO1", enable_events=True, default=False, key="-GreenChannel-"),
        sg.Radio("Blue", "RADIO1", enable_events=True, default=False, key="-BlueChannel-"),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Text("Brightness:"),
        sg.Push(),
        sg.Text("Contrast:")
    ],
    [
        sg.Slider(range=(-127, 127), enable_events=True, key="-BrightnessValue-", default_value=1, resolution=.1, size=(15,10), orientation='horizontal'),
        sg.Slider(range=(0.5,2), enable_events=True, key="-ContrastValue-", default_value=1, resolution=0.05,
                  size=(15,10), orientation='horizontal'),
    ],
    [
        sg.Text("Blur:"),
        sg.Slider(range=(1, 25), enable_events=True, key="-BlurValue-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Checkbox("ThresholdBinary", enable_events=True, key="-ThresholdBinary-"),
        sg.Slider(range=(0, 255), enable_events=True, key="-ThresholdValue-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [
        sg.Checkbox("Find contours", enable_events=True, key="-FindContours-")
    ],
    [
        sg.Checkbox("Approximation", enable_events=True, key="-ApproximationContours-"),
        sg.Slider(range=(0, 10), enable_events=True, key="-ApproximationValue-", default_value=4, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Text("Area:"),
        sg.Slider(range=(6, 100), enable_events=True, key="-AreaValue-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [
        sg.Checkbox("Triangle", enable_events=True, key="-Triangle-"),
        sg.Checkbox("Rectangle", enable_events=True, key="-Rectangle-"),
        sg.Checkbox("Round", enable_events=True, key="-Round-"),
    ],
    [
        sg.Text("The program found:"),
        sg.Text(size=(1,1), key='-OUTPUT-'),
        sg.Text("elements"),
    ],
    [
        sg.Checkbox("ThresholdBinary", enable_events=True, key="-ThresholdBinaryText-"),
        sg.Slider(range=(0, 255), enable_events=True, key="-ThresholdValueText-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
    [
        sg.Checkbox("Dilate", enable_events=True, key="-DilateText-"),
        sg.Slider(range=(0, 10), enable_events=True, key="-DilateText-", default_value=1, resolution=1, size=(15,10), orientation='horizontal'),
    ],
]

image_original_column = [
    [sg.Text("Choose an image from list:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    # [sg.Image(key="-IMAGE-")],
    [sg.Graph(
        canvas_size=(450, 450),
        graph_bottom_left=(0, 450),
        graph_top_right=(450, 0),
        key="-GRAPH-",
        enable_events=True,
        right_click_menu=[[], ['Erase item-Origin', ]]
    ), ]
]

image_OpenCV_column = [
    [sg.Text("Result of work OpenCV:")],
    [sg.Text(size=(40, 1), key="-TOUT_Converted-")],
    [sg.Graph(
        canvas_size=(450, 450),
        graph_bottom_left=(0, 450),
        graph_top_right=(450, 0),
        key="-NEW_GRAPH-",
        enable_events=True,
        # background_color=None,
        drag_submits=True,
        right_click_menu=[[], ['Erase item-CV2', ]]
    ), ]
]

layout = [
    [
        sg.Column(first_list_column, element_justification='c', size=(300, 700), scrollable=True),
        sg.VSeparator(),
        sg.Column(image_original_column),
        sg.VSeparator(),
        sg.Column(image_OpenCV_column),
    ]
]
