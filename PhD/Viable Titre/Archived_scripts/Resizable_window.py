import PySimpleGUI as sg

layout = [[sg.Text('My Window', key='-TEXT-', background_color='lightblue')],
          [sg.Input(key='-IN-'), sg.Text('', key='-OUT-')],
          [sg.Button('Do Something'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout, resizable=True)

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event == 'Do Something':
        print(f"The text element's size is {window['-TEXT-'].get_size()}")
        window['-TEXT-'].set_size((20, 3))
        window['-TEXT-'].Update('1\n2\n3')
        window.refresh()
        print(f"The text element's size is {window['-TEXT-'].get_size()}")
        window['Exit'].set_size((None, 2))       # Change only the height... one of the ONLY times None can be used in a size
window.close()
