# MySimplegui Viable Titre

import PySimpleGUI as sg
import numpy as np
import pandas as pd
from datetime import datetime

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")


# sg.theme_previewer()
# sg.theme_list()

# add window colour
sg.theme('DarkTeal9')

font = ('Calibri', 14)
font_small = ('Calibri', 12)

data=[]

# set the layout of the window
layout1 = [
    [sg.Text('Calculate the Viable Titre of your Strain:', font=font)],
    [sg.Text('Strain', size=(10, 1), font=font), sg.InputText(key='Strain', size=(15, 1), font=font)],
    [sg.Text('Condition', size=(10, 1), font=font), sg.Combo(['LB', 'Kan', 'Cm', 'Tc', 'Rif'], key='Condition', size=(15, 1), font=font)],
    [sg.Text('Volume plated (mL)', size=(10, 1), font=font), sg.Combo(['0.1', '0.01'], key='Volume', size=(15, 1), font=font)],
    [sg.Text('Dilution_1',  size=(10, 1), font=font),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution_1', size=(15, 1), font=font)],
    [sg.Text('Dilution_2',  size=(10, 1), font=font),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution_2', size=(15, 1), font=font)],
    [sg.Text('Colonies_1', size=(10, 1), font=font), sg.InputText(key='Colonies_1A', size=(15, 1), font=font),
        sg.InputText(key='Colonies_1B', size=(15, 1), font=font)],
    [sg.Text('Colonies_2', size=(10, 1), font=font), sg.InputText(key='Colonies_2A', size=(15, 1), font=font),
        sg.InputText(key='Colonies_2B', size=(15, 1), font=font)],
    [sg.Text('Viable Titre', size=(10, 1), font=font), sg.InputText('', key='Titre', size=(15, 1), font=font)],
    [sg.Text("Choose a spreadsheet to update: "), sg.FileBrowse(key='-FILE-')],
    [sg.Button('Calculate cells/mL', font=font), sg.Submit('Update Spreadsheet', font=font), sg.Button('Clear', font=font), sg.Exit(font=font)],
    [sg.Button('Open Spreadsheet')]
]

# recall the spreadsheet


def clear_input():
    for key in values:
        window[key]('')
    return None


# set empty results string for VT output
result = ''

# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1, size=(600, 450)) #size=(500, 500)

# while loop to keep the window up unless user closes it
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Calculate cells/mL':
        average1 = np.mean([int(values['Colonies_1A']), int(values['Colonies_1B'])])
        average2 = np.mean([int(values['Colonies_2A']), int(values['Colonies_2B'])])
        vol = float(values['Volume'])
        dilutions = np.sum([float(values['Dilution_1']), float(values['Dilution_2'])])
        result = np.sum([average1, average2]) / (vol * dilutions)
        window['Titre'].update(result)
    if event == 'Update Spreadsheet':
        EXCEL_FILE = values['-FILE-']
        df = pd.read_excel(EXCEL_FILE)
        df = df.append(values, ignore_index=True)
        df = df.drop(['-FILE-'], axis=1)
        df.to_excel(EXCEL_FILE, index=False)
        popup1 = sg.popup_yes_no('Do you want to save a separate csv file?')
        if popup1 == 'Yes':
            df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
        sg.popup('Data Saved!')
        # clear_input()
window.close()
