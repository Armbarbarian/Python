# MySimplegui Viable Titre

import PySimpleGUI as sg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")


# sg.theme_previewer()
# sg.theme_list()
# 'DarkTeal9', 'DarkGrey14', 'LightBlue2', 'LightBlue8'

# add window colour
sg.theme('DarkGrey14')

font = ('Calibri', 14)
font_small = ('Calibri', 12)

# set empty results string for VT output, paired with Calculate cells/mL
result = ''

# clear function paired with clear button


def clear_input():
    for key in values:
        window[key]('')
    return None


# empty lists paired with View Data button - see while true loop
data = []
header_list = []

# set the layout of the window
layout1 = [
    # [sg.Combo(['Light mode', 'Dark mode'], key='mode', change_submits=True, enable_events=True, pad=((400, 0), (0, 0)))], # set up light and dark mode feature
    [sg.Text('Calculate the Viable Titre of your Strain:', font=font)],
    [sg.Text('Strain', size=(10, 1), font=font),
        sg.InputText(key='Strain', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='1_check', change_submits=True, enable_events=True)],
    [sg.Text('Condition', size=(10, 1), font=font),
        sg.Combo(['LB', 'Kan', 'Cm', 'Tc', 'Rif'], key='Condition', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='2_check', change_submits=True, enable_events=True)],
    [sg.Text('Time (mins)', size=(10, 1), font=font),
        sg.Combo(['0', '30', '60', '90', '120', '150', '180'], key='Time', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='3_check', change_submits=True, enable_events=True)],
    [sg.Text('Volume (mL)', size=(10, 1), font=font),
        sg.Combo(['0.1', '0.01'], key='Volume', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='4_check', change_submits=True, enable_events=True)],
    [sg.Text('Dilution_1',  size=(10, 1), font=font),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution_1', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='5_check', change_submits=True, enable_events=True)],
    [sg.Text('Dilution_2',  size=(10, 1), font=font),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution_2', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='6_check', change_submits=True, enable_events=True)],
    [sg.Text('Colonies_1', size=(10, 1), font=font), sg.InputText(key='Colonies_1A', size=(15, 1), font=font),
        sg.InputText(key='Colonies_1B', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='7_check', change_submits=True, enable_events=True)],
    [sg.Text('Colonies_2', size=(10, 1), font=font), sg.InputText(key='Colonies_2A', size=(15, 1), font=font),
        sg.InputText(key='Colonies_2B', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='8_check', change_submits=True, enable_events=True)],
    [sg.Text('Viable Titre', size=(10, 1), font=font),
        sg.InputText('', key='Titre', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='9_check', change_submits=True, enable_events=True)],
    [sg.Text("Choose a spreadsheet to update: "), sg.FileBrowse(key='-FILE-')],
    [sg.Button('Calculate cells/mL', font=font), sg.Submit('Update Spreadsheet', font=font), sg.Button('Clear', font=font), sg.Exit(font=font)],
    [sg.Button('View Data', font=font)],
    [sg.Button('Plot Data', font=font)]
]


# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1)  # size=(600, 450)

# empty list to append checked keys into
checked = ['Strain', 'Condition', 'Time', 'Volume', 'Dilution_1', 'Dilution_2', 'Colonies_1A', 'Colonies_1B', 'Colonies_2A', 'Colonies_2B', 'Titre']

# while loop to keep the window up unless user closes it
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()

# enable the check boxes to disable the inputs
    if values['1_check'] == 0:
        window['Strain'].Update(disabled=True)
    if values['1_check'] == 1:
        window['Strain'].Update(disabled=False)
    if values['2_check'] == 0:
        window['Condition'].Update(disabled=True)
    if values['2_check'] == 1:
        window['Condition'].Update(disabled=False)
    if values['3_check'] == 0:
        window['Time'].Update(disabled=True)
    if values['3_check'] == 1:
        window['Time'].Update(disabled=False)
    if values['4_check'] == 0:
        window['Volume'].Update(disabled=True)
    if values['4_check'] == 1:
        window['Volume'].Update(disabled=False)
    if values['5_check'] == 0:
        window['Dilution_1'].Update(disabled=True)
    if values['5_check'] == 1:
        window['Dilution_1'].Update(disabled=False)
    if values['6_check'] == 0:
        window['Dilution_2'].Update(disabled=True)
    if values['6_check'] == 1:
        window['Dilution_2'].Update(disabled=False)
    if values['7_check'] == 0:
        window['Colonies_1A'].Update(disabled=True)
        window['Colonies_1B'].Update(disabled=True)
    if values['7_check'] == 1:
        window['Colonies_1A'].Update(disabled=False)
        window['Colonies_1B'].Update(disabled=False)
    if values['8_check'] == 0:
        window['Colonies_2A'].Update(disabled=True)
        window['Colonies_2B'].Update(disabled=True)
    if values['8_check'] == 1:
        window['Colonies_2A'].Update(disabled=False)
        window['Colonies_2B'].Update(disabled=False)
    if values['9_check'] == 0:
        window['Titre'].Update(disabled=True)
    if values['9_check'] == 1:
        window['Titre'].Update(disabled=False)

# append the key list which are highlighted
# Each if statement should update the checked list, not working currently
    if event == '1_check':
        if values['1_check'] == 0:
            checked.remove('Strain')
        elif values['1_check'] == 1:
            checked.append('Strain')
    if event == '2_check':
        if values['2_check'] == 0:
            checked.remove('Condition')
        elif values['2_check'] == 1:
            checked.append('Condition')
    if event == '3_check':
        if values['3_check'] == 0:
            checked.remove('Time')
        elif values['3_check'] == 1:
            checked.append('Time')
    if event == '4_check':
        if values['4_check'] == 0:
            checked.remove('Volume')
        if values['4_check'] == 1:
            checked.append('Volume')
    if event == '5_check':
        if values['5_check'] == 0:
            checked.remove('Dilution_1')
        if values['5_check'] == 1:
            checked.append('Dilution_1')
    if event == '6_check':
        if values['6_check'] == 0:
            checked.remove('Dilution_2')
        if values['6_check'] == 1:
            checked.append('Dilution_2')
    if event == '7_check':
        if values['7_check'] == 0:
            checked.remove('Colonies_1A')
            checked.remove('Colonies_1B')
        if values['7_check'] == 1:
            checked.append('Colonies_1A')
            checked.append('Colonies_1B')
    if event == '8_check':
        if values['8_check'] == 0:
            checked.remove('Colonies_2A')
            checked.remove('Colonies_2B')
        if values['8_check'] == 1:
            checked.append('Colonies_2A')
            checked.append('Colonies_2B')
    if event == '9_check':
        if values['9_check'] == 0:
            checked.remove('Titre')
        if values['9_check'] == 1:
            checked.append('Titre')

    # calculate the viable titre and output on screen
    if event == 'Calculate cells/mL':
        try:
            average1 = np.mean([int(values['Colonies_1A']), int(values['Colonies_1B'])])
            average2 = np.mean([int(values['Colonies_2A']), int(values['Colonies_2B'])])
            vol = float(values['Volume'])
            dilutions = np.sum([float(values['Dilution_1']), float(values['Dilution_2'])])
            result = np.sum([average1, average2]) / (vol * dilutions)
            window['Titre'].update(result)
        except:
            sg.popup('Not enough data provided')

# saving xlsx and csv file with cleaned data
    if event == 'Update Spreadsheet':
        try:
            EXCEL_FILE = values['-FILE-']
            df = pd.read_excel(EXCEL_FILE)

        # keep only columns that have been appended to checked list
            df = df.append(values, ignore_index=True)

        # This drops the names of the check boxes if NOT in checked list
            df = df.drop(columns=[col for col in df if col not in checked])
            df.to_excel(EXCEL_FILE, index=False)
            popup1 = sg.popup_yes_no('Do you want to save a separate csv file?')
            if popup1 == 'Yes':
                df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
                sg.popup('Data Saved!')
        except:
            sg.popup('No file selected')
    if event == 'View Data':
        try:
            CSV_FILE = ('output_'+day+'-'+month+'.csv')
            CSV_DF = pd.read_csv(CSV_FILE)
        # retrieve a list of the values in the csv file
            data = CSV_DF.values.tolist()
        # retrieve list of column names
            header_list = list(CSV_DF.columns)
            sg.popup('Data found!')
            layout_data = [
                [sg.Table(values=data, headings=header_list, display_row_numbers=False, auto_size_columns=False,
                          num_rows=min(25, len(data)), alternating_row_color='teal')]  # teal, lightblue
            ]
            window_data = sg.Window('output_'+day+'-'+month+'.csv', layout_data)
            event, values = window_data.read()
        except:
            sg.popup_error('YOU DIED')
            window.close()

# plotting the data (not ready yet)
    if event == 'Plot Data':
        sg.popup('Feature not ready')
        try:
            print('Hello')
        except:
            sg.popup('You Died')
        # clear_input()
window.close()
