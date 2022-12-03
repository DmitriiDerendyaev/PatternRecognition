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
        sg.Radio("Find on photo", enable_events=True, key="-FIRST_IMG-", group_id="RADIO_01", default=False),
        sg.Radio("Find in web", enable_events=True, key="-SECOND_IMG-", group_id="RADIO_01", default= False)
    ],
    [
        sg.Radio("OFF", enable_events=True, key="-OFF-", group_id="RADIO_01", default= True)
    ]
]

image_original_column = [
    [sg.Text("Choose an image from list:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
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