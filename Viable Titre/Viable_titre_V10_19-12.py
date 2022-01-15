# MySimplegui Viable Titre
from PIL import Image
import csv
import io
import os
from datetime import datetime
import PySimpleGUI as sg
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
os.getcwd()
# %matplotlib inline
matplotlib.use('TkAgg')
plt.style.use('ggplot')

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

# list to append checked keys into
checked = ['Strain', 'Condition', 'Time', 'Volume', 'Dilution_1', 'Dilution_2', 'Colonies_1A', 'Colonies_1B', 'Colonies_2A', 'Colonies_2B', 'Titre']

# clear function paired with clear button


def clear_input():
    for key in checked:
        window[key]('')
    return None


# empty lists paired with View Data button - see while true loop
data = []
header_list = []


# function for the plot figure
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# list of markers for home screen
markers = ['LB', 'Kan', 'Cm', 'Tc', 'Tm', 'Apra', 'Amp', 'Rif']


# pre render term image to show in mutaiton rates
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


# https://stackoverflow.com/questions/58692537/use-png-files-from-a-dictionary-to-display-in-a-image-widget-in-pysimplegui-pyt
def get_img_data(f, maxsize=(1200, 850)):
    '''
    uses PIL to generate data from the image
    '''
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    del img
    return bio.getvalue()


# median find nearest function
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


# set the layout of the window
layout1 = [
    # [sg.Combo(['Light mode', 'Dark mode'], key='mode', change_submits=True, enable_events=True, pad=((400, 0), (0, 0)))], # set up light and dark mode feature
    [sg.Text('Calculate the Viable Titre of your Strain:', font=font)],
    [sg.Text('Strain', size=(10, 1), font=font),
        sg.InputText(key='Strain', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='1_check', change_submits=True, enable_events=True)],
    [sg.Text('Condition', size=(10, 1), font=font),
        sg.Combo(markers, key='Condition', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='2_check', change_submits=True, enable_events=True)],
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
    [sg.Button('Calculate cells/mL', font=font, pad=((0, 0), (0, 0))), sg.Button('Clear', font=font)],
    [sg.Text('Viable Titre', size=(10, 1), font=font),
        sg.InputText('', key='Titre', size=(15, 1), font=font, disabled=False), sg.Checkbox('', default=1, key='9_check', change_submits=True, enable_events=True)],
    [sg.Text('_'*65)],
    [sg.Text("Choose an existing spreadsheet to update: ", font=font), sg.FileBrowse(key='-FILE-')],
    [sg.Submit('Create New Spreadsheet', font=font), sg.Submit('Update Spreadsheet', font=font)],
    [sg.Text('_'*65)],
    [sg.Text('Other Tools:', font=font)],
    [sg.Button('View Data', font=font, button_color='darkcyan'), sg.Button('Analyse Data', font=font, button_color='darkcyan'),
        sg.Exit(font=font, button_color='firebrick', size=(10, 1), pad=((150, 0), (0, 0)))]
]


# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1, resizable=True, finalize=True)  # size=(600, 450)

# while loop to keep the window up unless user closes it and asks if you want to close
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        close_popup = sg.popup_yes_no('Have you saved your work?', font=font)
        if close_popup == 'No':
            continue
        else:
            break

# Resize window options to stop callbacks
    elif event == 'Configure':
        if window.TKroot.state() == 'zoomed':
            status.update(value='Window zoomed and maximized !')
        else:
            status.update(value='Window normal')

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
    if event == 'Create New Spreadsheet':
        popup2 = sg.popup_yes_no('Do you want to save a separate csv file?', font=font)
        try:
            if popup2 == 'Yes':
                df = pd.DataFrame()
                df = df.append(values, ignore_index=True)
                df = df.drop(columns=[col for col in df if col not in checked])
                df.to_excel('output_'+day+'-'+month+'.xlsx')
                df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
                sg.popup('XLSX and CSV Files created, set to todays date')
        except:
            df = pd.DataFrame()
            df = df.append(values, ignore_index=True)
            df = df.drop(columns=[col for col in df if col not in checked])
            df.to_excel('output_'+day+'-'+month+'.xlsx')
            sg.popup('XLSX File created, set to todays date')

    if event == 'Update Spreadsheet':
        try:
            EXCEL_FILE = values['-FILE-']
            df = pd.read_csv(EXCEL_FILE)
            # keep only columns that have been appended to checked list
            df = df.append(values, ignore_index=True)
            # This drops the names of the check boxes if NOT in checked list
            df = df.drop(columns=[col for col in df if col not in checked])
            df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
            sg.popup('Data Saved!')
        except:
            EXCEL_FILE = 'output_'+day+'-'+month+'.csv'
            df = pd.read_csv(EXCEL_FILE)
            # keep only columns that have been appended to checked list
            df = df.append(values, ignore_index=True)
            # This drops the names of the check boxes if NOT in checked list
            df = df.drop(columns=[col for col in df if col not in checked])
            df.to_csv(EXCEL_FILE, index=False)
            popup1 = sg.popup_yes_no('Appended CSV?', font=font)
            if popup1 == 'Yes':
                df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
                sg.popup('CSV appended')
            if popup1 == 'No':
                continue


# Viewing the data saved under Output
    if event == 'View Data':
        auto_manual_selection = sg.popup_yes_no('Do you want to manually select the file?', font=font)
        if auto_manual_selection == 'No':
            try:
                CSV_FILE = ('output_'+day+'-'+month+'.csv')
                CSV_DF = pd.read_csv(CSV_FILE)
            # retrieve a list of the values in the csv file
                data = CSV_DF.values.tolist()
            # retrieve list of column names
                header_list = list(CSV_DF.columns)
                # sg.popup('Data found!')
                layout_data = [
                    [sg.Table(values=data, headings=header_list, font=font, key='Viewed_data', display_row_numbers=False, auto_size_columns=False,
                              num_rows=min(25, len(data)), alternating_row_color='teal', enable_events=True), sg.Button('Append Spreadsheet', key='-Append_csv-', font=font)],  # teal, lightblue
                ]
                window_data = sg.Window('output_'+day+'-'+month+'.csv', layout_data, resizable=True, finalize=True)
                event, values = window_data.read()
            except:
                sg.popup_error('YOU DIED')
                window.close()
        else:
            if auto_manual_selection == 'Yes':
                browse_file_layout = [
                    [sg.Text('Select your csv file:', font=font), sg.FileBrowse(key='csv_file', font=font)],
                    [sg.Submit(key='csv_submit', font=font)]
                ]
                browse_csv_window = sg.Window('Find the csv file to display', browse_file_layout)
                event, values = browse_csv_window.read()
                if event == 'csv_submit':
                    CSV_FILE_input = values['csv_file']
                    CSV_DF_input = pd.read_csv(CSV_FILE_input)
                # retrieve a list of the values in the csv file
                    data_input = CSV_DF_input.values.tolist()
                # retrieve list of column names
                    header_list_input = list(CSV_DF_input.columns)
                    # sg.popup('Data input found!')
                    browse_csv_window.close()
                    layout_data_input = [
                        [sg.Table(values=data_input, headings=header_list_input, font=font, display_row_numbers=False, auto_size_columns=False,
                                  num_rows=min(25, len(data_input)), alternating_row_color='RoyalBlue')]  # teal, lightblue
                    ]
                    window_data_input = sg.Window('Your csv data displayed', layout_data_input, resizable=True, finalize=True)
                    event, values = window_data_input.read()
        if event == '-Append_csv-':
            sg.popup('Feature not available')

# plotting the data (not ready yet)
    if event == 'Analyse Data':
        empty_data = []
        empty_heading = []
        analysis_layout = [
            [sg.Text('Select a csv of your data:',  font=font, size=(20, 0)), sg.FileBrowse(key='csv_file2')],
            [sg.Text('Select type of analysis', font=font, size=(20, 0)), sg.Combo(
                ['Growth Curve', 'Stand Alone Titre Comparison', 'Calculate Median Culture', 'Mutation Rates'], key='analysis_type', size=(25, 1), font=font)],
            [sg.Submit('Select Analysis', font=font), sg.Text(' or ', font=font), sg.Submit('Plot Data', font=font)],
            [sg.Text('_'*80)]
        ]
        window_analysis_question = sg.Window('Analysis', analysis_layout, resizable=True, finalize=True)
        while True:
            event, values = window_analysis_question.read()
            if event == sg.WIN_CLOSED:
                break
            # sg.popup('Feature not ready')
            if event == 'Select Analysis':
                # Growth curve analysis
                if values['analysis_type'] == 'Growth Curve':
                    sg.popup('Growth Curve Analysis not ready yet', font=font)
                    continue

            # Stand alone titre analysis
                if values['analysis_type'] == 'Stand Alone Titre Comparison':
                    sg.popup('Stand Alone Titre Comparison not ready yet', font=font)

            # Median calculation (Recombination rates)
                if values['analysis_type'] == 'Calculate Median Culture':
                    try:
                        master_df = pd.read_csv(values['csv_file2'])
                        headings2 = list(master_df.columns)
                        data_input2 = master_df.values.tolist()
                        data_strain = master_df.Strain.tolist()
                        data_titre = master_df.Titre.tolist()

                        median_heading = ['Culture', 'Titre']
                    except:
                        sg.popup('No file selected', font=font)
                        continue

                    # window_analysis_question['-Cultures Text-'].Update(visible=True)
                    # window_analysis_question['-Cultures Dropdown-'].Update(visible=True)

# Specifying up to 8 side by side strains being cultured.
# Update them depending on the values of the Strain Dropdown
# organised in column format for easier viewing and layout
                    Strains_col1 = [
                        [sg.Text('Strain 1 row start', key='-1start_text-', font=font, visible=False),
                         sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-1start-', font=font, visible=False)],
                        [sg.Text('Strain 2 row start', key='-2start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-2start-', font=font, visible=False)],
                        [sg.Text('Strain 3 row start', key='-3start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-3start-', font=font, visible=False)],
                        [sg.Text('Strain 4 row start', key='-4start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-4start-', font=font, visible=False)]
                    ]

                    Strains_col2 = [
                        [sg.Text('Strain 1 row stop', key='-1stop_text-', font=font, visible=False),
                         sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-1stop-', font=font, visible=False)],
                        [sg.Text('Strain 2 row stop', key='-2stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-2stop-', font=font, visible=False)],
                        [sg.Text('Strain 3 row stop', key='-3stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-3stop-', font=font, visible=False)],
                        [sg.Text('Strain 4 row stop', key='-4stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-4stop-', font=font, visible=False)]
                    ]

                    Strains_col3 = [
                        [sg.Text('Strain 5 row start', key='-5start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-5start-', font=font, visible=False)],
                        [sg.Text('Strain 6 row start', key='-6start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-6start-', font=font, visible=False)],
                        [sg.Text('Strain 7 row start', key='-7start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-7start-', font=font, visible=False)],
                        [sg.Text('Strain 8 row start', key='-8start_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-8start-', font=font, visible=False)]
                    ]

                    Strains_col4 = [
                        [sg.Text('Strain 5 row stop', key='-5stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-5stop-', font=font, visible=False)],
                        [sg.Text('Strain 6 row stop', key='-6stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-6stop-', font=font, visible=False)],
                        [sg.Text('Strain 7 row stop', key='-7stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-7stop-', font=font, visible=False)],
                        [sg.Text('Strain 8 row stop', key='-8stop_text-', font=font, visible=False), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-8stop-', font=font, visible=False)]
                    ]

                    analysis_table_layout = [
                        [sg.Text('Select the rows to calculate the median from:')],
                        [sg.Table(values=data_input2, headings=headings2, key='-Median Table-', font=font, display_row_numbers=True, auto_size_columns=False,
                                  num_rows=min(10, len(data_input2)), alternating_row_color='RoyalBlue', visible=True,
                                  enable_events=False)],
                        [sg.Text('Set up some parameters first:', key='-param Text-', font=font, visible=True)],
                        [sg.Text('how many cultures do you have?', key='-Cultures Text-', font=font, visible=True), sg.Combo(list(range(1, 12)), key='-Cultures Dropdown-', font=font, visible=True)],
                        [sg.Text('how many strains do you have?', key='-Strains Text-', font=font, visible=True), sg.Combo(list(range(1, 12)),
                                                                                                                           key='-Strains Dropdown-', font=font, visible=True), sg.Button('Go', key='paramButton', visible=True, disabled=False)],
                        [sg.Column(Strains_col1, background_color='lightgray'), sg.Column(Strains_col2, background_color='lightgray'),
                         sg.Column(Strains_col3, background_color='gray'), sg.Column(Strains_col4, background_color='gray')],
                        [sg.Submit('Calculate', font=font), sg.Exit('Close', font=font, button_color='firebrick')],
                        [sg.Text('', key='strain1_median_culture', font=font, visible=False), sg.Text('', key='strain1_median_titre', font=font, visible=False)],
                        # output of concat dfs showing median
                        [sg.Table(values=data_input2, headings=median_heading, key='-Median output-', font=font, display_row_numbers=False, num_rows=4, auto_size_columns=False, background_color='green', visible=False,
                                  enable_events=False),
                         sg.Button('Add to CSV', key='AddButton', visible=False)]
                    ]

                    window_median_table = sg.Window('Median Calculation', analysis_table_layout, resizable=True, finalize=True)
                    window_analysis_question.close()
                    while True:
                        event, values = window_median_table.read()
                        if event == 'paramButton':
                            window_median_table['paramButton'].Update(disabled=True)
                            NumCultures = int(values['-Cultures Dropdown-'])
                            NumStrains = int(values['-Strains Dropdown-'])


# There must be another way to simplify the code below to update the rows as we need them
# Some conditional based on the number of Strains provided


# Number of Strains if then conditions
                            if NumStrains >= 1:
                                window_median_table['-1start_text-'].Update(visible=True)
                                window_median_table['-1stop_text-'].Update(visible=True)
                                window_median_table['-1start-'].Update(visible=True)
                                window_median_table['-1stop-'].Update(visible=True)
                            if NumStrains >= 2:
                                window_median_table['-2start_text-'].Update(visible=True)
                                window_median_table['-2stop_text-'].Update(visible=True)
                                window_median_table['-2start-'].Update(visible=True)
                                window_median_table['-2stop-'].Update(visible=True)
                            if NumStrains >= 3:
                                window_median_table['-3start_text-'].Update(visible=True)
                                window_median_table['-3stop_text-'].Update(visible=True)
                                window_median_table['-3start-'].Update(visible=True)
                                window_median_table['-3stop-'].Update(visible=True)
                            if NumStrains >= 4:
                                window_median_table['-4start_text-'].Update(visible=True)
                                window_median_table['-4stop_text-'].Update(visible=True)
                                window_median_table['-4start-'].Update(visible=True)
                                window_median_table['-4stop-'].Update(visible=True)
                            if NumStrains >= 5:
                                window_median_table['-5start_text-'].Update(visible=True)
                                window_median_table['-5stop_text-'].Update(visible=True)
                                window_median_table['-5start-'].Update(visible=True)
                                window_median_table['-5stop-'].Update(visible=True)
                            if NumStrains >= 6:
                                window_median_table['-6start_text-'].Update(visible=True)
                                window_median_table['-6stop_text-'].Update(visible=True)
                                window_median_table['-6start-'].Update(visible=True)
                                window_median_table['-6stop-'].Update(visible=True)
                            if NumStrains >= 7:
                                window_median_table['-7start_text-'].Update(visible=True)
                                window_median_table['-7stop_text-'].Update(visible=True)
                                window_median_table['-7start-'].Update(visible=True)
                                window_median_table['-7stop-'].Update(visible=True)
                            if NumStrains >= 8:
                                window_median_table['-8start_text-'].Update(visible=True)
                                window_median_table['-8stop_text-'].Update(visible=True)
                                window_median_table['-8start-'].Update(visible=True)
                                window_median_table['-8stop-'].Update(visible=True)


# The below calculations and appending a dataframe work, but are restricted in the sense that
# I have to code how many strains are mentioned.
# I need to allow for a condition based on how many strains we have as mentioned above.

# Calculating the Median
                        if event == 'Calculate':
                            NumStrain_NameList = []
                            NumStrain_Df = pd.DataFrame()
                            # user input
                            if NumStrains >= 1:
                                strain1_row_start = values['-1start-']
                                strain1_row_stop = values['-1stop-']
                                try:
                                    temp_names1 = list(master_df.Strain[strain1_row_start:strain1_row_stop])
                                    temp_titre1 = list(master_df.Titre[strain1_row_start:strain1_row_stop])
                                    temp_df1 = pd.DataFrame({'names': temp_names1, 'titre': temp_titre1})
                                    data_temp1 = temp_df1.sort_values(by='titre')
                                    median1 = data_temp1['titre'].median()
                                    nearest_median1 = find_nearest(data_temp1['titre'], median1)
                                    median_culture1 = data_temp1.loc[data_temp1['titre'] == nearest_median1]
                                    NumStrain_NameList.append(median_culture1.iloc[0, 0])
                                    NumStrain_Df = NumStrain_Df.append(median_culture1)
                                    # sg.popup(NumStrain_list)
                                except:
                                    sg.popup('Error: Select rows from top to bottom only.', font=font)
                                    continue
                                # sg.popup('1st check', font=font)

                            if NumStrains >= 2:
                                strain2_row_start = values['-2start-']
                                strain2_row_stop = values['-2stop-']
                                try:
                                    temp_names2 = list(master_df.Strain[strain2_row_start:strain2_row_stop])
                                    temp_titre2 = list(master_df.Titre[strain2_row_start:strain2_row_stop])
                                    temp_df2 = pd.DataFrame({'names': temp_names2, 'titre': temp_titre2})
                                    data_temp2 = temp_df2.sort_values(by='titre')
                                    median2 = data_temp2['titre'].median()
                                    nearest_median2 = find_nearest(data_temp2['titre'], median2)
                                    median_culture2 = data_temp2.loc[data_temp2['titre'] == nearest_median2]
                                    NumStrain_NameList.append(median_culture2.iloc[0, 0])
                                    NumStrain_Df = NumStrain_Df.append(median_culture2)
                                except:
                                    sg.popup('Error: Select rows from top to bottom only.', font=font)
                                    continue
                                # sg.popup('2nd check', font=font)

                            if NumStrains >= 3:
                                strain3_row_start = values['-3start-']
                                strain3_row_stop = values['-3stop-']
                                try:
                                    temp_names3 = list(master_df.Strain[strain3_row_start:strain3_row_stop])
                                    temp_titre3 = list(master_df.Titre[strain3_row_start:strain3_row_stop])
                                    temp_df3 = pd.DataFrame({'names': temp_names3, 'titre': temp_titre3})
                                    data_temp3 = temp_df3.sort_values(by='titre')
                                    median3 = data_temp3['titre'].median()
                                    nearest_median3 = find_nearest(data_temp3['titre'], median3)
                                    median_culture3 = data_temp3.loc[data_temp3['titre'] == nearest_median3]
                                    NumStrain_NameList.append(median_culture3.iloc[0, 0])
                                    NumStrain_Df = NumStrain_Df.append(median_culture3)
                                except:
                                    sg.popup('Error: Select rows from top to bottom only.', font=font)
                                    continue
                                # sg.popup('3rd check', font=font)

                            if NumStrains >= 4:
                                strain4_row_start = values['-4start-']
                                strain4_row_stop = values['-4stop-']
                                try:
                                    temp_names4 = list(master_df.Strain[strain4_row_start:strain4_row_stop])
                                    temp_titre4 = list(master_df.Titre[strain4_row_start:strain4_row_stop])
                                    temp_df4 = pd.DataFrame({'names': temp_names4, 'titre': temp_titre4})
                                    data_temp4 = temp_df4.sort_values(by='titre')
                                    median4 = data_temp4['titre'].median()
                                    nearest_median4 = find_nearest(data_temp4['titre'], median4)
                                    median_culture4 = data_temp4.loc[data_temp4['titre'] == nearest_median4]
                                    NumStrain_NameList.append(median_culture4.iloc[0, 0])
                                    NumStrain_Df = NumStrain_Df.append(median_culture4)
                                except:
                                    sg.popup('Error: Select rows from top to bottom only.', font=font)
                                    continue

                            if NumStrains >= 5:
                                strain5_row_start = values['-5start-']
                                strain5_row_stop = values['-5stop-']
                                try:
                                    temp_names5 = list(master_df.Strain[strain5_row_start:strain5_row_stop])
                                    temp_titre5 = list(master_df.Titre[strain5_row_start:strain5_row_stop])
                                    temp_df5 = pd.DataFrame({'names': temp_names5, 'titre': temp_titre5})
                                    data_temp5 = temp_df5.sort_values(by='titre')
                                    median5 = data_temp5['titre'].median()
                                    nearest_median5 = find_nearest(data_temp5['titre'], median5)
                                    median_culture5 = data_temp5.loc[data_temp5['titre'] == nearest_median5]
                                    NumStrain_NameList.append(median_culture5.iloc[0, 0])
                                    NumStrain_Df = NumStrain_Df.append(median_culture5)
                                except:
                                    sg.popup('Error: Select rows from top to bottom only.', font=font)
                                    continue

                            if NumStrains >= 6:
                                strain6_row_start = values['-6start-']
                                strain6_row_stop = values['-6stop-']
                                try:
                                    temp_names6 = list(master_df.Strain[strain6_row_start:strain6_row_stop])
                                    temp_titre6 = list(master_df.Titre[strain6_row_start:strain6_row_stop])
                                    temp_df6 = pd.DataFrame({'names': temp_names6, 'titre': temp_titre6})
                                    data_temp6 = temp_df6.sort_values(by='titre')
                                    median6 = data_temp6['titre'].median()
                                    nearest_median6 = find_nearest(data_temp6['titre'], median6)
                                    median_culture6 = data_temp6.loc[data_temp6['titre'] == nearest_median6]
                                    NumStrain_NameList.append(median_culture6.iloc[0, 0])
                                    NumStrain_Df = NumStrain_Df.append(median_culture6)
                                except:
                                    sg.popup('Error: Select rows from top to bottom only.', font=font)
                                    continue
                                # sg.popup('4th check', font=font)

                            sg.popup(NumStrain_Df)

                            median_list = NumStrain_Df.values.tolist()
                            # median1_heading = temp_df1.columns.tolist() # trouble updating the headings
                            # median2_heading = temp_df2.columns.tolist()

                        # appending the table to show the median cultures
                        # show the button to update the spreadhseet
                            window_median_table['-Median output-'].Update(values=median_list, visible=True)
                            window_median_table['AddButton'].Update(visible=True)

                            sg.popup('Now make a note of the median cultures', font=font)


# This needs to be more streamline to add True or False in the correct column to be called
# Later when retrieving the median cultures, this way we won't have to make more csv files
# which keeps the process cleaner.

                        if event == 'AddButton':
                            try:
                                # CSV_FILE = ('output_'+day+'-'+month+'.csv')
                                CSV_DF = master_df

                                # cult1_strain = NumStrain_NameList[1]
                                # cult2_strain = NumStrain_NameList[2]
                                # cult3_strain = NumStrain_NameList[3]
                                # cult4_strain = NumStrain_NameList[4]
                            except:
                                sg.popup('check 1')

                            try:
                                # joined_cult = cult1_strain + cult2_strain + cult3_strain + cult4_strain
                                sg.popup(NumStrain_NameList)
                                indexes = []
                        # Retreiving the cultures that are the median values
                                for strain1 in NumStrain_NameList:
                                    if strain1 in CSV_DF.values:
                                        indices1 = str(CSV_DF[CSV_DF['Strain'] == strain1].index.values)
                                        if indices1 not in indexes:
                                            indexes.append(indices1)
                            except:
                                sg.popup('check 2')

                            try:
                                if 'Median' not in CSV_DF.columns:  # LO here trying to add more than two cultures
                                    CSV_DF['Median'] = 'NA'
                                else:
                                    continue
                                for strain in NumStrain_NameList:
                                    CSV_DF.loc[CSV_DF.Strain == strain, 'Median'] = 'True'
                                CSV_DF.to_csv('MEDIAN_output'+'_'+day+'-'+month+'.csv')
                                sg.popup('Data has been added!', font=font)
                            except:
                                sg.popup('check 3')

                        if event == sg.WIN_CLOSED or event == 'Close':
                            break
                    window_median_table.close()
                    continue
                    # save the selected rows into a df
                    # new_data1 = values['-Median Table-']
                    # closing and exiting the median window

# _____________________________________________________________________________________________
#                                                                               Mutation Rates
                if values['analysis_type'] == 'Mutation Rates':
                    window_analysis_question.close()
                    try:
                        master_df = pd.read_csv(values['csv_file2'])
                        headings2 = list(master_df.columns)
                        data_input2 = master_df.values.tolist()
                        data_strain = master_df.Strain.tolist()
                        data_titre = master_df.Titre.tolist()
                        median_heading = ['Culture', 'Titre']

                        # selecting the antibiotic drop down
                        antibiotics_list = []
                        data_antibiotics = master_df.Condition
                        for con in data_antibiotics:
                            if con not in antibiotics_list:
                                antibiotics_list.append(con)

                        # selecting only the median strains for the dropdown later for '-Median_culture1-'
                        medians_list = []
                        data_medians = master_df.loc[master_df['Median'] == True].Strain
                        for strain in data_medians:
                            if strain not in medians_list:
                                medians_list.append(strain)

                    except:
                        sg.popup('Median Spreadsheet must be used...', font=font)
                        # headings3 = list(master_df.columns)
                        # data_input3 = master_df.values.tolist()
                        # data_strain = master_df.Strain.tolist()
                        # continue
                    mutation_layout_text = [
                        [sg.Text('Specify your parameters below:', font=font, key='-parameters_text-', visible=True)],
                        [sg.Text('_'*20, key='-divider1-')],  # divider
                        [sg.Text('Median Culture Name:', font=font, key='-Name_text-', visible=True)],
                        [sg.Text('Antibiotic Used:', font=font, key='-Antibiotic_text-', visible=True)],
                        [sg.Text('Plated Volume:', font=font, key='-Volume_text-', visible=True)],
                        [sg.Text('Mutation Rate Calculation:', key='-Rate_text-', visible=True)],
                        [sg.Text('Number of Cultures (N):', font=font, key='-Number_text-', visible=True)],
                        [sg.Button('Retrieve Strain and Calculate', visible=True)],
                        [sg.Text('_'*20)],
                        [sg.Text('Cell Count per Culture (n):', font=font, key='-Count_text-', visible=True)],
                        [sg.Text('Mutation Events per Culture (r\N{SUBSCRIPT ZERO}):', font=font, key='-Events_text-', visible=True)],
                        # [sg.Text('Fraction of mutants:', font=font)], # same as Mrates
                        [sg.Text('Mutation Rate \u03BC (Fraction):', font=font, key='-u_text-', visible=True)],
                        [sg.Text('Mutation Rate (m):', font=font, key='-m_text-', visible=True)],
                        [sg.Text('Sigma Value:', font=font, key='-s_text-', visible=True)],
                        [sg.Text('Sigma / m:', font=font, key='-sm_text-', visible=True)],
                        [sg.Text('m / n:', font=font, key='-mn_text-', visible=True)],
                        [sg.Text('Sigma / n:', font=font, key='-sn_text-', visible=True)]
                    ]

                    mutation_layout_input = [
                        [sg.Text(' '*20)],
                        [sg.Combo(medians_list, key='-Median_culture1-', size=(10, 1), font=font, visible=True)],
                        [sg.Combo(antibiotics_list, key='-Ab-', size=(10, 1), font=font, visible=True)],
                        [sg.Combo(['0.1', '0.01'], key='-Vol-', size=(10, 1), font=font, visible=True)],
                        [sg.Combo(['Method 1 (Drake): \u03BC = m / Nt', 'Method 2: \u03BC = m / (Nt-1)', 'Method 3: \u03BC = m / 2Nt',
                                  'Method 4: \u03BC = m ln(2) / Nt'], key='-Mrate_method-', enable_events=True, visible=True)],
                        [sg.InputText(key='-Cultures-', size=(20, 1), font=font, visible=True)],
                        [sg.Text(' '*20)],
                        [sg.Text(' '*20)],
                        [sg.InputText(key='-Cells-', size=(20, 1), font=font, visible=True)],
                        [sg.InputText(key='-Mutations-', size=(20, 1), font=font, visible=True)],
                        # [sg.InputText(key='-Fraction-', size=(20, 1), font=font)], # same as Mrates
                        [sg.InputText(key='-Mrates-', size=(20, 1), font=font, visible=True)],
                        [sg.InputText(key='-Mrates_m-', size=(20, 1), font=font, visible=True)],
                        [sg.InputText(key='-Sigma-', size=(20, 1), font=font, visible=True)],
                        [sg.InputText(key='-s/m-', size=(20, 1), font=font, visible=True)],
                        [sg.InputText(key='-m/n-', size=(20, 1), font=font, visible=True)],
                        [sg.InputText(key='-s/n-', size=(20, 1), font=font, visible=True)]
                    ]

                    mutation_layout = [
                        [[sg.Column(mutation_layout_text),
                         sg.Column(mutation_layout_input, pad=((0, 0), (40, 0))),
                          sg.Button('View Terms', font=font, pad=((0, 0), (0.0))),
                          sg.Image(key='-Terms-', visible=False), sg.Button('Close Image', key='-close_image-', visible=False)],
                         [sg.Button('Save Mutation Data', font=font), sg.Exit(font=font, button_color='firebrick', size=(10, 1), pad=((330, 0), (0, 0)))],
                         [sg.Button('Compare Two Strains', font=font, button_color='teal')],
                         [sg.Text('_'*30, key='-divider10-', visible=False)],
                         [sg.Text('Strain 1:', key='-strain1-', visible=False),
                            sg.Combo(data_strain, key='-strain1_dropdown-', visible=False)],
                         [sg.Text('Strain 2:', key='-strain2-', visible=False),
                         sg.Combo(data_strain, key='-strain2_dropdown-', visible=False)],
                         ]]

                    mutation_window = sg.Window('Mutation Rates', mutation_layout, resizable=True, finalize=True)
                    while True:
                        event, values = mutation_window.read()
                        if event == sg.WIN_CLOSED or event == 'Exit':
                            mutation_window.close()
                            break
                        if event == 'Retrieve Strain and Calculate':
                            try:
                                found_strain1 = master_df.loc[master_df['Strain'] == values['-Median_culture1-']]
                            # cleaning the dataframe to get our median with 100uL plated
                                true_medianstrain1 = found_strain1[found_strain1.Volume == float(values['-Vol-'])]
                                # values['-Vol-']
                                LB_strain1 = true_medianstrain1[true_medianstrain1.Condition == 'LB']
                                Ab_strain1 = true_medianstrain1[true_medianstrain1.Condition == values['-Ab-']]

                                LB_titre = LB_strain1.Titre
                                Ab_titre = Ab_strain1.Titre

                                LB_total_cells1 = LB_titre*5
                                Ab_total_cells1 = Ab_titre*5

                        # Calculations for mutation rates, all slightly different
                                # Fraction = Ab_titre.item() / LB_titre.item()
                                Mrates_classic = Ab_total_cells1.item() / LB_total_cells1.item()
                                # print(Mrates_classic)
                                # m = np.log(Mrates)

                                if values['-Mrate_method-'] == 'Method 1 (Drake): \u03BC = m / Nt':
                                    Mrates = Ab_total_cells1.item() / LB_total_cells1.item()
                                elif values['-Mrate_method-'] == 'Method 2: \u03BC = m / (Nt-1)':
                                    Mrates = Ab_total_cells1.item() / (LB_total_cells1.item() - 1)
                                elif values['-Mrate_method-'] == 'Method 3: \u03BC = m / 2Nt':
                                    Mrates = Ab_total_cells1.item() / (2 * LB_total_cells1.item())
                                elif values['-Mrate_method-'] == 'Method 4: \u03BC = m ln(2) / Nt':
                                    Mrates = (Ab_total_cells1.item() * np.log(2)) / LB_total_cells1.item()
                                else:
                                    sg.popup('Something wrong with rate method...')
                                # print(Mrates)

                        # Calculate m number and sigma value here
                        # This replaces the need for the Javascript program! completed 23/09/21
                        # ________________________________________________________________________

                                iter = 1e-8
                                N = float(values['-Cultures-'])
                                n = LB_total_cells1.item()
                                m = Ab_total_cells1.item()
                                u = Mrates_classic

                                # mutation number
                                m0 = 0.0
                                r0 = m
                                while (np.abs(m0 - m) >= iter):
                                    m0 = m
                                    divident = (1.24 * m0) + (m0 * np.log(m0)) - r0
                                    divisor = 2.24 + np.log(m0)
                                    m = m0 - (divident / divisor)

                                # sigma value
                                divident_s = 12.7
                                divisor_s = (2.24 + np.log(m)) * (2.24 + np.log(m))
                                sigma = m * np.sqrt((1/N) * (divident_s/divisor_s))

                                # Sigma / m
                                s_m = sigma / m

                                # m/ n
                                m_n = m / n

                                # Sigma / n
                                s_n = sigma / n

                        # ________________________________________________________________________

                        # Update the input fields showing the number of cells
                        # .item() retrieved the actual value
                                mutation_window['-Cells-'].Update(LB_total_cells1.item())
                                mutation_window['-Mutations-'].Update(Ab_total_cells1.item())
                                # mutation_window['-Fraction-'].Update(Fraction)
                                mutation_window['-Mrates-'].Update(Mrates)
                                mutation_window['-Mrates_m-'].Update(m)
                                mutation_window['-Sigma-'].Update(sigma)
                                mutation_window['-s/m-'].Update(s_m)
                                mutation_window['-m/n-'].Update(m_n)
                                mutation_window['-s/n-'].Update(s_n)

                            except:
                                sg.popup('No such strain found')

                        mutation_file = []  # set blank then update on next run through.
                        if event == 'Save Mutation Data':
                            popup2 = sg.popup_yes_no('Do you want to append an existing file?')
                            mutation_dict = {'Strain': [values['-Median_culture1-']],
                                             'Cultures': [values['-Cultures-']],
                                             'Total_cells': [values['-Cells-']],
                                             'Mutant_cells': [values['-Mutations-']],
                                             'Rate_u': [values['-Mrates-']],
                                             'Rate_m': [values['-Mrates_m-']],
                                             'Sigma': [values['-Sigma-']],
                                             'Sigma_m': [values['-s/m-']],
                                             'm_n': [values['-m/n-']],
                                             'Sigma_n': [values['-s/n-']]}
                            if popup2 == 'No':
                                try:
                                    mutation_dataframe = pd.DataFrame(mutation_dict)
                                    mutation_dataframe.to_csv(('mutationrate'+day+'-'+month+'.csv'), index=False)
                                    sg.popup('New file saved!')
                                except:
                                    sg.popup('Something went wrong.')
                            if popup2 == 'Yes':
                                try:
                                    df1 = pd.read_csv(mutation_file)
                                    mutation_dataframe = pd.DataFrame(mutation_dict)
                                    df1 = df1.append(mutation_dataframe, ignore_index=True)
                                    df1.to_csv((mutation_file), index=False)
                                    sg.popup('Data saved!')
                                except:
                                    browse_file_layout = [
                                        [sg.Text('Select your csv file:'), sg.FileBrowse(key='mutation_file')],
                                        [sg.Submit(key='csv_submit')]
                                    ]
                                    browse_csv_window = sg.Window('Find the csv file to display', browse_file_layout)
                                    event, values = browse_csv_window.read()
                                    if event == 'csv_submit':
                                        mutation_file = values['mutation_file']
                                        df1 = pd.read_csv(mutation_file)
                                        mutation_dataframe = pd.DataFrame(mutation_dict)
                                        df1 = df1.append(mutation_dataframe, ignore_index=True)
                                        df1.to_csv((mutation_file), index=False)
                                        sg.popup('Data saved!')
                                        browse_csv_window.close()
                                        continue
                        if event == 'View Terms':
                            try:
                                wd = os.getcwd()
                                FILE = 'Foster2006_terms.png'
                                rendered = get_img_data(FILE)
                                term_layout = [
                                    [sg.Image(key='-Terms-')],
                                    [sg.Exit('Close', font=font)]
                                ]
                                if event == 'Close' or event == sg.WIN_CLOSED:
                                    break
                                if os.path.exists(FILE):
                                    image = Image.open(FILE)
                                    image.thumbnail((600, 600))
                                    bio = io.BytesIO()
                                    image.save(bio, format="PNG")
                                    mutation_window['-Terms-'].update(data=bio.getvalue())
                                    mutation_window['-close_image-'].update(visible=True)
                                    mutation_window['-Terms-'].update(visible=True)

                            except:
                                sg.popup('Not working')
                        # Allow for opening and closing the image at will
                        if event == '-close_image-':
                            mutation_window['-Terms-'].update(visible=False)
                            mutation_window['-close_image-'].update(visible=False)

                        # Calculating the factor between two strains
                        if event == 'Compare Two Strains':
                            # make the comparison entry info visible
                            mutation_window['-strain1-'].Update(visible=True)
                            mutation_window['-strain2-'].Update(visible=True)
                            mutation_window['-strain1_dropdown-'].Update(visible=True)
                            mutation_window['-strain2_dropdown-'].Update(visible=True)
                            mutation_window['-divider1-'].Update(visible=True)

                            # make the OG calculation info invisible
                            mutation_window['-Cultures-'].Update(visible=False)
                            mutation_window['-Cells-'].Update(visible=False)
                            mutation_window['-Mutations-'].Update(visible=False)
                            mutation_window['-Mrates-'].Update(visible=False)
                            mutation_window['-Mrates_m-'].Update(visible=False)
                            mutation_window['-Sigma-'].Update(visible=False)
                            mutation_window['-s/m-'].Update(visible=False)
                            mutation_window['-m/n-'].Update(visible=False)
                            mutation_window['-s/n-'].Update(visible=False)
                            # _____________________________________________________
                            mutation_window['-parameters_text-'].Update(visible=False)
                            mutation_window['-Name_text-'].Update(visible=False)
                            mutation_window['-Antibiotic_text-'].Update(visible=False)
                            mutation_window['-Volume_text-'].Update(visible=False)
                            mutation_window['-Rate_text-'].Update(visible=False)
                            mutation_window['Retrieve Strain'].Update(visible=False)
                            mutation_window['-Number_text-'].Update(visible=False)
                            mutation_window['-Events_text-'].Update(visible=False)
                            mutation_window['-u_text-'].Update(visible=False)
                            mutation_window['-m_text-'].Update(visible=False)
                            mutation_window['-s_text-'].Update(visible=False)
                            mutation_window['-sm_text-'].Update(visible=False)
                            mutation_window['-mn_text-'].Update(visible=False)
                            mutation_window['-sn_text-'].Update(visible=False)

                        # sample
                            '''
                            [sg.Text('Specify your parameters below:', font=font, key='-parameters_text-', visible=True)],
                            [sg.Text('_'*20)],  # divider
                            [sg.Text('Median Culture Name:', font=font, key='-Name_text-', visible=True)],
                            [sg.Text('Antibiotic Used:', font=font, key='-Antibiotic_text-', visible=True)],
                            [sg.Text('Plated Volume:', font=font, key='-Volume_text-', visible=True)],
                            [sg.Text('Mutation Rate Calculation:', key='-Rate_text-', visible=True)],
                            [sg.Button('Retrieve Strain', visible=True)],
                            [sg.Text('_'*20)],
                            [sg.Text('Number of Cultures (N):', font=font, key='-Number_text-', visible=True)],
                            [sg.Text('Cell Count per Culture (n):', font=font, key='-Count_text-', visible=True)],
                            [sg.Text('Mutation Events per Culture (r\N{SUBSCRIPT ZERO}):', font=font, key='-Events_text-', visible=True)],
                            # [sg.Text('Fraction of mutants:', font=font)], # same as Mrates
                            [sg.Text('Mutation Rate \u03BC (Fraction):', font=font, key='-u_text-', visible=True)],
                            [sg.Text('Mutation Rate (m):', font=font, key='-m_text-', visible=True)],
                            [sg.Text('Sigma Value:', font=font, key='-s_text-', visible=True)],
                            [sg.Text('Sigma / m:', font=font, key='-sm_text-', visible=True)],
                            [sg.Text('m / n:', font=font, key='-mn_text-', visible=True)],
                            [sg.Text('Sigma / n:', font=font, key='-sn_text-', visible=True)]
                            '''

                            # left off here trying to append the csv to get an update mutation rate df which is just copied from the 1998 html prog.
                            # clear_input()

            # View plot for any individual dataset
            if event == 'Plot Data':
                plot_window_layout = [
                    [sg.Text('Browse the file to create the plot', font=font)],
                    [sg.FileBrowse(key='csv_file2')],
                    [sg.Button('Load it!', font=font)],
                    [sg.Text('Specify The Parameters of The Plot', font=font)],
                    [sg.Text('Select Plot type: ', font=font),
                        sg.Combo(values=['Line', 'Bar', 'Scatter'],  key='-dropdown_plot-', font=font)],
                    [sg.Text('Title: ', font=font), sg.InputText(key='-input_title-')],
                    [sg.Text('Select X Values: ', font=font),
                        sg.Combo(values=[], key='-dropdown_x-', size=(20, 1), font=font)],
                    [sg.Text('Select Y Values: ', font=font),
                        sg.Combo(values=[], key='-dropdown_y-', size=(20, 1), font=font)],
                    [sg.Text('X Label: ', font=font),
                        sg.InputText(key='-Xlab-', size=(20, 1), font=font)],
                    [sg.Text('Y Label: ', font=font),
                        sg.InputText(key='-Ylab-', size=(20, 1), font=font)],
                    [sg.Text('label rotation: '),
                        sg.Combo(values=list(range(0, 91, 5)), key='-rotation-', font=font)],
                    [sg.Text('Width: '),
                        sg.Combo(list(range(0, 30)), key='-fig_w-', font=font),
                        sg.Text('Height: '),
                        sg.Combo(list(range(0, 30)), key='-fig_h-', font=font)],
                    [sg.Text('Custom X labels: '),
                        sg.InputText(key='-xticks-', font=font)],
                    [sg.Text('Custom bar colours: '),
                        sg.InputText(key='-colours-', font=font)],
                    [sg.Button('Graph it!', font=font, button_color='green'),
                        sg.Button('Exit', font=font, button_color='firebrick')]

                ]

                plot_window = sg.Window('Plot data', plot_window_layout, resizable=True, finalize=True)
                while True:
                    event, values = plot_window.read()
                    if event == sg.WIN_CLOSED or event == 'Exit':
                        plot_window.close()
                        break
                    if event == 'Load it!':
                        try:
                            '''
                            # for plotting - can't get working
                            with open(values['csv_file2']) as master_df:
                                master_reader = csv.DictReader(master_df)
                            row = next(master_reader)
                            '''
                            master_df = pd.read_csv(values['csv_file2'])
                            new_list = list(master_df.columns)
                            tempt_list = new_list
                            Strain_list = list(master_df['Strain'])
                            # plot_window['-strain1-'].Update(values=Strain_list)
                            # plot_window['-strain2-'].Update(values=Strain_list)
                            plot_window['-dropdown_x-'].Update(values=new_list)
                            plot_window['-dropdown_y-'].Update(values=new_list)
                        except:
                            sg.popup('FAIL')

                    # Make and show the graph
                    if event == 'Graph it!':

                        if values['-dropdown_plot-'] == 'Bar':
                            try:  # The better way to generate and customise the plot using pyplot
                                def graph_main():
                                    fig = plt.figure()
                                    colors = ['royalblue', 'darkorchid', 'firebrick', 'darkgreen', 'darkred', 'navy']
                                    x = master_df[str(values['-dropdown_x-'])].tolist()
                                    y = master_df[str(values['-dropdown_y-'])].tolist()
                                    errors = master_df['Sigma_n'].tolist()

                                    #plt.bar(x, y, color=colors[:len(x)], yerr=errors, ecolor='black', capsize=5)
                                    plt.title(values['-input_title-'])
                                    # X label
                                    if not values['-Xlab-']:
                                        plt.xlabel(values['-dropdown_x-'], fontsize=14)
                                    else:
                                        plt.xlabel(values['-Xlab-'], fontsize=14)
                                    # Y label
                                    if not values['-Ylab-']:
                                        plt.ylabel(values['-dropdown_y-'], fontsize=14)
                                    else:
                                        plt.ylabel(values['-Ylab-'], fontsize=14)
                                    # X rotation
                                    if not values['-rotation-']:
                                        plt.xticks(rotation=0, ha='center')
                                    else:
                                        plt.xticks(rotation=values['-rotation-'], ha='right')

                                    plt.grid(True)
                                    plt.legend(fontsize=14)
                                    fig = plt.gcf()
                                    try:
                                        if values['-fig_w-'] > 0:
                                            fig.set_size_inches(values['-fig_w-'], values['-fig_h-'])
                                    except:
                                        fig.set_size_inches(5, 5)

                                    # Custom Xticks
                                    if not values['-xticks-']:
                                        pass
                                    else:
                                        x_list = values['-xticks-'].split(', ')
                                        plt.xticks(range(len(Strain_list)), x_list)

                                    # Custom bar colours
                                    if not values['-colours-']:
                                        plt.bar(x, y, color=colors[:len(x)], yerr=errors, ecolor='black', capsize=5)
                                    else:
                                        colors_input = values['-colours-'].split(', ')
                                        plt.bar(x, y, color=colors_input, yerr=errors, ecolor='black', capsize=5)

                                    fig.tight_layout()  # autosizes the plot Really handy
                                    fig.show()
                                graph_main()

                            except:  # the basic way using inbuilt pandas method if the above doesn't work.
                                sg.popup('Except Loop started')

                                def graph_alt():
                                    master_df.plot.bar(x=values['-dropdown_x-'], y=values['-dropdown_y-'], color='royalblue')
                                    plt.title('Title')
                                    plt.xlabel(values['-dropdown_x-'], fontsize=12)
                                    plt.ylabel(values['-dropdown_y-'], fontsize=12)
                                    # plt.grid(True)
                                    # plt.legend(fontsize=14)
                                    plt.show()
                                graph_alt()

                        if values['-dropdown_plot-'] == 'Line':
                            try:
                                def graph_real():
                                    x = master_df[[values['-dropdown_x-']]]
                                    y = master_df[[values['-dropdown_y-']]]
                                    plt.plot(x, y, marker='o')
                                    plt.title('Title')
                                    plt.xlabel(values['-dropdown_x-'], fontsize=14)
                                    plt.ylabel(values['-dropdown_y-'], fontsize=14)
                                    plt.grid(True)
                                    plt.legend(fontsize=14)
                                    # plt.savefig('2021_enzymes_graph1.png')
                                    plt.show()
                                graph_real()
                            except:
                                sg.popup('FAIL')
                                continue

                        if values['-dropdown_plot-'] == 'Scatter':
                            sg.popup('Under construction.. choose another plot')


window.close()


##########################################################################################
#
#                                         TEST SPACE
#
##########################################################################################

dict = {'Strain': [1, 2, 3], 'total': [20, 30, 40], 'median': [True, False, False]}
df = pd.DataFrame(dict)
df
csv = pd.read_csv('mutationrate19-12.csv')
df = pd.DataFrame(dict)
x = csv['Strain'].tolist()
x
y = csv['m_n'].tolist()
y
plt.bar(x, y)
# plt.show()


# manual calculations
iter = 1e-8
N = 9
n = 1304545455
m = 8954
u = 6.86E-06


# This replaces the need for the Javascript program! completed 23/09/21
m0 = 0.0
r0 = m
while (np.abs(m0 - m) >= iter):
    m0 = m
    divident = (1.24 * m0) + (m0 * np.log(m0)) - r0
    divisor = 2.24 + np.log(m0)
    m = m0 - (divident / divisor)
    print(m)  # mutation rate is not the same as in the html program
m

# sigma value
# from HTML
divident_s = 12.7
divisor_s = (2.24 + np.log(m)) * (2.24 + np.log(m))
s = m * np.sqrt((1/N) * (divident_s/divisor_s))
s


# mutationrate from the 1998 program in JavaScript
'''
from the mutation rate program in what looks like javascript to calculate mutation rate

# mutation rate
// Mutationsrate berechnen...
function MutationBerechnen()
{
   var m0 = 0.0, r0 = this.m;
   while (Math.abs(m0 - this.m) >= this.grenze)
   {
      m0 = this.m;
      divident = (1.24 * m0) + (m0 * Math.log(m0)) - r0;
      divisor  = 2.24 + Math.log(m0);
      this.m = m0 - (divident / divisor);
   }
}

# sigma
function SigmaBerechnen()
{
   divident = 12.7;
   divisor =  (2.24 + Math.log(this.m)) * (2.24 + Math.log(this.m));
   this.s = this.m * Math.sqrt((1/this.N) * (divident/divisor));
}
'''

# retrieving index for the median values in the dataframe to append/add with button
# https://www.edureka.co/community/43215/how-to-find-the-index-of-a-particular-value-in-a-dataframe
'''
CSV_FILE = ('output_'+day+'-'+month+'.csv')
CSV_DF = pd.read_csv(CSV_FILE)
CSV_DF
xlist = ['DG011 #5', 'DG011 #6', 'DG012 #5']
indexes = []
for strain in xlist:
    if strain in CSV_DF.values:
        indices = str(CSV_DF[CSV_DF['Strain'] == strain].index.values)
        if indices not in xlist:
            indexes.append(indices)
    else:
        print('not here')
# print(indexes)
'''


# matplotlib of mutation rates
dict = {'A': [1, 2, 3],
        'B': [4, 5, 6]}
pd.DataFrame(dict)

# WT and Tus-
x = ['SLM1042', 'SLM1043', 'DG011', 'DG012']
x_pos = [i for i, _ in enumerate(x)]
y_raw = [7E-07, 2.23E-06, 6E-07, 8E-07]
y_factor = [1, 1.87, 0.729, 1.38]

plt.bar(x_pos, y_factor, color='blue')
plt.xlabel('Strains')
plt.ylabel('Factor increase in recombination')
plt.title('Rates of Recombination in single origin E.coli')
plt.xticks(x_pos, x)

# oriX and oriZ
x = ['DG023', 'DG024', 'DG025', 'DG026']
x_pos = [i for i, _ in enumerate(x)]
y_raw = [1.7E-06, 1.12E-06, 5.06E-06, 5.47E-06]
y_factor = [0.846, 0.397, 1, 1.62]

plt.bar(x_pos, y_factor, color='blue')
plt.xlabel('Strains')
plt.ylabel('Factor increase in recombination')
plt.title('Rates of Recombination in single origin E.coli')
plt.xticks(x_pos, x)

# combination of the two
x = ['WT ter', 'WT ctrl', 'OriX ter', 'OriX ctrl', 'OriZ ter', 'OriZ ctrl']
x_pos = [i for i, _ in enumerate(x)]
y_raw = [7E-07, 2.23E-06, 5.06E-06, 5.47E-06]
y_factor = [(7E-07/7E-07), (2.23E-06/7E-07), (1.7E-06/7E-07), (1.12E-06/7E-07), (5.06E-06/7E-07), (5.47E-06/7E-07)]
errors = [9.09E-08*1E6, 3.00E-07*1E6, 3.66E-07*1E6, 2.61E-07*1E6, 1.07E-06*1E6, 1.10E-06*1E6]
fig = plt.figure()
fig.patch.set_facecolor('white')
# fig.patch.set_alpha(0.6)
plt.bar(x_pos, y_factor, color=['royalblue', 'royalblue', 'purple', 'purple', 'darkred', 'darkred'], yerr=errors, ecolor='black', capsize=5)
plt.xlabel('Strains')
plt.ylabel('Factor increase in recombination')
plt.title('Preliminary Rates of Recombination in E.coli\nwith varying number of origins')
plt.xticks(x_pos, x)
plt.grid(b=None)


# plt.savefig('Recombination_rates_Ecoli_1.png')
# plt.savefig('Recombination_rates_Ecoli_1.pdf')
