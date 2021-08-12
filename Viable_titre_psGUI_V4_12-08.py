# MySimplegui Viable Titre

import PySimpleGUI as sg
import pandas as pd

# sg.theme_previewer()
# sg.theme_list()

# add window colour
sg.theme('DarkTeal9')
EXCEL_FILE = 'out_VT_12-08.xlsx'
df = pd.read_excel(EXCEL_FILE)
df

# set the layout of the window
layout1 = [
    [sg.Text('Calculate the Viable Titre of your Strain:')],
    [sg.Text('Strain', size=(10, 1)), sg.InputText(key='Strain', size=(10, 1))],
    [sg.Text('Condition', size=(10, 1)), sg.Combo(['LB', 'Kan', 'Cm', 'Tc', 'Rif'], key='Condition', size=(10, 1))],
    [sg.Text('Dilution',  size=(10, 1)),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution', size=(10, 1))],
    [sg.Text('Colonies_A', size=(10, 1)), sg.InputText(key='Colonies_A', size=(10, 1))],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()]
]

# clear function button


def clear_input():
    for key in values:
        window[key]('')
    return None

# add more boxes and calculations etc....


# set up the window and the layout to use for the window
window = sg.Window('Viable Titre PySimpleGUI', layout1, size=(500, 300))

# while loop to keep the window up unless user closes it
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        #print(event, values)
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data Saved!')
        clear_input()
window.close()
