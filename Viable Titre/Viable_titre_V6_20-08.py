# MySimplegui Viable Titre

from datetime import datetime
import PySimpleGUI as sg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
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

# clear function paired with clear button


def clear_input():
    for key in values:
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
    [sg.Button('Analyse Data', font=font)]
]


# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1)  # size=(600, 450)

# empty list to append checked keys into
checked = ['Strain', 'Condition', 'Time', 'Volume', 'Dilution_1', 'Dilution_2', 'Colonies_1A', 'Colonies_1B', 'Colonies_2A', 'Colonies_2B', 'Titre']

# median find nearest function


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


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

# Viewing the data saved under Output
    if event == 'View Data':
        auto_manual_selection = sg.popup_yes_no('Do you want to manually select the file?')
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
                              num_rows=min(25, len(data)), alternating_row_color='teal')]  # teal, lightblue
                ]
                window_data = sg.Window('output_'+day+'-'+month+'.csv', layout_data)
                event, values = window_data.read()
            except:
                sg.popup_error('YOU DIED')
                window.close()
        else:
            if auto_manual_selection == 'Yes':
                browse_file_layout = [
                    [sg.Text('Select your csv file:'), sg.FileBrowse(key='csv_file')],
                    [sg.Submit(key='csv_submit')]
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
                        [sg.Table(values=data_input, headings=header_list_input, display_row_numbers=False, auto_size_columns=False,
                                  num_rows=min(25, len(data_input)), alternating_row_color='RoyalBlue')]  # teal, lightblue
                    ]
                    window_data_input = sg.Window('Your csv data displayed', layout_data_input)
                    event, values = window_data_input.read()
# plotting the data (not ready yet)
    if event == 'Analyse Data':
        empty_data = []
        empty_heading = []
        analysis_layout = [
            [sg.Text('Select a csv of your data:',  font=font, size=(20, 0)), sg.FileBrowse(key='csv_file2')],
            [sg.Text('Select type of analysis', font=font, size=(20, 0)), sg.Combo(
                ['Growth Curve', 'Stand Alone Titre Comparison', 'Calculate Median Culture'], key='analysis_type', size=(25, 1), font=font)],
            [sg.Submit('Select Analysis', font=font)],
            [sg.Text('_'*80)],
            [sg.Text('how many cultures do you have?', key='-Cultures Text-', font=font, visible=False), sg.Combo(list(range(1, 11)), key='-Cultures Dropdown-', font=font, visible=False)]
        ]
        window_analysis_question = sg.Window('Analysis', analysis_layout)
        event, values = window_analysis_question.read()
        if event == sg.WIN_CLOSED:
            continue
        # sg.popup('Feature not ready')
        if event == 'Select Analysis':

            if values['analysis_type'] == 'Calculate Median Culture':
                master_df = pd.read_csv(values['csv_file2'])
                headings2 = list(master_df.columns)
                data_input2 = master_df.values.tolist()
                data_strain = master_df.Strain.tolist()
                data_titre = master_df.Titre.tolist()

                median_heading = ['Culture', 'Titre']

                # window_analysis_question['-Cultures Text-'].Update(visible=True)
                # window_analysis_question['-Cultures Dropdown-'].Update(visible=True)
                analysis_table_layout = [
                    [sg.Text('Select the rows to calculate the median from:')],
                    [sg.Table(values=data_input2, headings=headings2, key='-Median Table-', font=font, display_row_numbers=True, auto_size_columns=False,
                              num_rows=min(10, len(data_input2)), alternating_row_color='RoyalBlue', visible=True,
                              enable_events=False)],
                    [sg.Text('Strain 1:', key='strain1', visible=True, font=font), sg.InputText(key='Median_strain1', size=(10, 0), font=font, visible=True)],
                    [sg.Text('Strain 2:', key='strain2', visible=True, font=font), sg.InputText(key='Median_strain2', size=(10, 0), font=font, visible=True)],

                    [sg.Text('Strain 1 row start', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-1start-', font=font), sg.Text('Strain 1 row stop', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-1stop-', font=font),
                     sg.Text('Strain 2 row start', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-2start-', font=font), sg.Text('Strain 2 row stop', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-2stop-', font=font)],


                    [sg.Submit('Calculate', font=font), sg.Exit('Close', key='close', font=font)],

                    [sg.Text('', key='strain1_median_culture', font=font, visible=False), sg.Text('', key='strain1_median_titre', font=font, visible=False)],
                    [sg.Text('', key='strain2_median_culture', font=font, visible=False), sg.Text('', key='strain2_median_titre', font=font, visible=False)],

                    # output of concat dfs showing median
                    [sg.Table(values=data_input2, headings=median_heading, key='-Median output-', font=font, display_row_numbers=False, num_rows=2, auto_size_columns=False, background_color='green', visible=False,
                              enable_events=False)]
                ]
                window_median_table = sg.Window('Median Calculation', analysis_table_layout)
                event, values = window_median_table.read()

                if event == sg.WIN_CLOSED:
                    continue
                if event == 'close':
                    continue

                if event == 'Calculate':
                    # user input
                    strain1_row_start = values['-1start-']
                    strain1_row_stop = values['-1stop-']
                    strain2_row_start = values['-2start-']
                    strain2_row_stop = values['-2stop-']
                    strain1_name = values['Median_strain1']
                    strain2_name = values['Median_strain2']

                # Actually calculating the median from the input rows given
                    temp_names1 = list(master_df.Strain[strain1_row_start:strain1_row_stop])
                    temp_names2 = list(master_df.Strain[strain2_row_start:strain2_row_stop])
                    temp_titre1 = list(master_df.Titre[strain1_row_start:strain1_row_stop])
                    temp_titre2 = list(master_df.Titre[strain2_row_start:strain2_row_stop])
                    temp_df1 = pd.DataFrame({'names': temp_names1, 'titre': temp_titre1})
                    temp_df2 = pd.DataFrame({'names': temp_names2, 'titre': temp_titre2})
                    data_temp1 = temp_df1.sort_values(by='titre')
                    data_temp2 = temp_df2.sort_values(by='titre')
                    median1 = data_temp1['titre'].median()
                    median2 = data_temp2['titre'].median()
                # find the nearest value
                    nearest_median1 = find_nearest(data_temp1['titre'], median1)
                    nearest_median2 = find_nearest(data_temp2['titre'], median2)
                # filter the OG dataframe to return the culture with that value
                    median_culture1 = data_temp1.loc[data_temp1['titre'] == nearest_median1]
                    median_culture2 = data_temp2.loc[data_temp2['titre'] == nearest_median2]
                    # concatenate the two dfs to show only one table
                    median_concat = pd.concat([median_culture1, median_culture2], axis=0, ignore_index=True)
                #
                    median_list = median_concat.values.tolist()
                    # median1_heading = temp_df1.columns.tolist() # trouble updating the headings
                    #median2_heading = temp_df2.columns.tolist()

                # appending the table to show the median cultures
                window_median_table['-Median output-'].Update(values=median_list, visible=True)

                # save the selected rows into a df
                # new_data1 = values['-Median Table-']

                # closing and exiting the median window
            continue
        else:
            sg.popup('This type of analysis is not ready yet...')
            window_analysis_question.close()


# clear_input()
window.close()


''' # plotting the data - work this out later
plt.scatter(data_temp1.names, data_temp1.titre, color='RoyalBlue')
plt.xlabel('Culture')
plt.ylabel('Cells/mL')
plt.title('SLM1043 Cultures')
plt.xticks(rotation=75)'''
