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
    ]