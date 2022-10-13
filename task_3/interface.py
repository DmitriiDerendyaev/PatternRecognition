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
        sg.Checkbox("Bilinear filtering", default=False, enable_events=True, key="-Bilinear-"),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Radio("Scalling", "RADIO1", enable_events=True, default=False, key="-Scalling-"),
    ],
    [
        sg.Text("X:"),
        sg.Slider(range=(0.1, 3), enable_events=True, key="-ScallingX-", default_value=1, resolution=0.05,
                  size=(12, 10), orientation='horizontal'),
        sg.Text("Y:"),
        sg.Slider(range=(0.1, 3), enable_events=True, key="-ScallingY-", default_value=1, resolution=0.05,
                  size=(12, 10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
[
        sg.Radio("Shearing", "RADIO1", enable_events=True, default=False, key="-Shearing-"),
    ],
    [
        sg.Text("X:"),
        sg.Slider(range=(-1, 1), enable_events=True, key="-ShearingX-", default_value=0, resolution=0.05,
                  size=(12, 10), orientation='horizontal'),
        sg.Text("Y:"),
        sg.Slider(range=(-1, 1), enable_events=True, key="-ShearingY-", default_value=0, resolution=0.05,
                  size=(12, 10), orientation='horizontal'),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Radio("Rotation", "RADIO1", enable_events=True, default=False, key="-Rotation-"),
    ],
    [
        sg.Text("Angle:"),
        sg.Slider(range=(0, 3.14), enable_events=True, key="-Angle-", default_value=1, resolution=0.05,
                  size=(25, 10), orientation='horizontal'),
    ],
    # [
    #     sg.Text("Y:"),
    #     sg.Slider(range=(0.1, 3), enable_events=True, key="-RotationY-", default_value=1, resolution=0.05,
    #               size=(12, 10), orientation='horizontal'),
    # ],
    [sg.HorizontalSeparator()],
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
        background_color='lightblue',
        # background_color=None,
        drag_submits=True,
        right_click_menu=[[], ['Erase item', ]]
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
        background_color='lightblue',
        # background_color=None,
        drag_submits=True,
        right_click_menu=[[], ['Erase item', ]]
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
