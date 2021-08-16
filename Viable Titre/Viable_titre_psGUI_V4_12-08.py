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

# add window colour
sg.theme('DarkTeal9')

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
    [sg.Text('Calculate the Viable Titre of your Strain:', font=font)],
    [sg.Text('Strain', size=(10, 1), font=font),
        sg.InputText(key='Strain', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='1_check', change_submits = True, enable_events=True)],
    [sg.Text('Condition', size=(10, 1), font=font),
        sg.Combo(['LB', 'Kan', 'Cm', 'Tc', 'Rif'], key='Condition', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='2_check', change_submits = True, enable_events=True)],
    [sg.Text('Time (mins)', size=(10, 1), font=font),
        sg.Combo(['0', '30', '60', '90', '120', '150', '180'], key='Time', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='3_check', change_submits = True, enable_events=True)],
    [sg.Text('Volume (mL)', size=(10, 1), font=font),
        sg.Combo(['0.1', '0.01'], key='Volume', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='4_check', change_submits = True, enable_events=True)],
    [sg.Text('Dilution_1',  size=(10, 1), font=font),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution_1', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='5_check', change_submits = True, enable_events=True)],
    [sg.Text('Dilution_2',  size=(10, 1), font=font),
        sg.Combo(['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8'], key='Dilution_2', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='6_check', change_submits = True, enable_events=True)],
    [sg.Text('Colonies_1', size=(10, 1), font=font), sg.InputText(key='Colonies_1A', size=(15, 1), font=font),
        sg.InputText(key='Colonies_1B', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='7_check', change_submits = True, enable_events=True)],
    [sg.Text('Colonies_2', size=(10, 1), font=font), sg.InputText(key='Colonies_2A', size=(15, 1), font=font),
        sg.InputText(key='Colonies_2B', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='8_check', change_submits = True, enable_events=True)],
    [sg.Text('Viable Titre', size=(10, 1), font=font),
        sg.InputText('', key='Titre', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='9_check', change_submits = True, enable_events=True)],
    [sg.Text("Choose a spreadsheet to update: "), sg.FileBrowse(key='-FILE-')],
    [sg.Button('Calculate cells/mL', font=font), sg.Submit('Update Spreadsheet', font=font), sg.Button('Clear', font=font), sg.Exit(font=font)],
    [sg.Button('View Data', font=font)],
    [sg.Button('Plot Data', font=font)]
]


# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1) #size=(600, 450)

# empty list to append checked keys into
checked = []

# while loop to keep the window up unless user closes it
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if values['1_check'] == 0:
        window['Strain'].Update(disabled = True)
    if values['1_check'] == 1:
        window['Strain'].Update(disabled = False)
        try:
            checked.append(['Strain']) # need a way to not duplicate the key LO 16/08
            print(checked)
        except:
            print('NOPE')
    if values['2_check'] == 0:
        window['Condition'].Update(disabled = True)
    if values['2_check'] == 1:
        window['Condition'].Update(disabled = False)
    if values['3_check'] == 0:
        window['Time'].Update(disabled = True)
    if values['3_check'] == 1:
        window['Time'].Update(disabled = False)
    if values['4_check'] == 0:
        window['Volume'].Update(disabled = True)
    if values['4_check'] == 1:
        window['Volume'].Update(disabled = False)
    if values['5_check'] == 0:
        window['Dilution_1'].Update(disabled = True)
    if values['5_check'] == 1:
        window['Dilution_1'].Update(disabled = False)
    if values['6_check'] == 0:
        window['Dilution_2'].Update(disabled = True)
    if values['6_check'] == 1:
        window['Dilution_2'].Update(disabled = False)
    if values['7_check'] == 0:
        window['Colonies_1A'].Update(disabled = True)
    if values['7_check'] == 1:
        window['Colonies_1A'].Update(disabled = False)
    if values['7_check'] == 0:
        window['Colonies_1B'].Update(disabled = True)
    if values['7_check'] == 1:
        window['Colonies_1B'].Update(disabled = False)
    if values['8_check'] == 0:
        window['Colonies_2A'].Update(disabled = True)
    if values['8_check'] == 1:
        window['Colonies_2A'].Update(disabled = False)
    if values['8_check'] == 0:
        window['Colonies_2B'].Update(disabled = True)
    if values['8_check'] == 1:
        window['Colonies_2B'].Update(disabled = False)
    if values['9_check'] == 0:
        window['Titre'].Update(disabled = True)
    if values['9_check'] == 1:
        window['Titre'].Update(disabled = False)
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
        #df = df.append(values, ignore_index=True)
        # Trying to only keep columns which are checked
        #df = df.drop(['-FILE-'], axis=1)
        df = df.drop(['-FILE-', '1_check', '2_check', '3_check', '4_check', '5_check', '6_check', '7_check', '8_check', '9_check'], axis='columns')
        df.to_excel(EXCEL_FILE, index=False)
        popup1 = sg.popup_yes_no('Do you want to save a separate csv file?')
        if popup1 == 'Yes':
            df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
        sg.popup('Data Saved!')
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
                [sg.Table(values=data, headings=header_list, display_row_numbers=False, auto_size_columns=False, num_rows=min(25, len(data)), alternating_row_color='teal')]
            ]
            window_data = sg.Window('output_'+day+'-'+month+'.csv', layout_data)
            event, values = window_data.read()
        except:
            sg.popup_error('YOU DIED')
            window.close()
    if event == 'Plot Data':
        sg.popup('Feature not ready')
        '''
        try:
            print('Hello')
        except:
            sg.popup('You Died')'''
        # clear_input()
window.close()
