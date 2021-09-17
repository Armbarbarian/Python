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

# empty list to append checked keys into
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


markers = ['LB', 'Kan', 'Cm', 'Tc', 'Tm', 'Apra', 'Amp', 'Rif']


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
    [sg.Text("Choose a spreadsheet to update: ", font=font), sg.FileBrowse(key='-FILE-')],
    [sg.Submit('Update Spreadsheet', font=font)],
    [sg.Text('_'*65)],
    [sg.Text('Other Tools:', font=font)],
    [sg.Button('View Data', font=font, button_color='darkcyan'), sg.Button('Analyse Data', font=font, button_color='darkcyan'),
        sg.Exit(font=font, button_color='firebrick', size=(10, 1), pad=((150, 0), (0, 0)))]
]


# set up the window and the layout to use for the window
window = sg.Window('Viable Titre GUI', layout1)  # size=(600, 450)

# median find nearest function


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


# while loop to keep the window up unless user closes it and asks if you want to close
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        close_popup = sg.popup_yes_no('Have you saved your work?', font=font)
        if close_popup == 'No':
            continue
        else:
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
            popup1 = sg.popup_yes_no('Do you want to save a separate csv file?', font=font)
            if popup1 == 'Yes':
                df.to_csv(('output_'+day+'-'+month+'.csv'), index=False)
                sg.popup('Data Saved!')
        except:
            sg.popup('No file selected')

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
                              num_rows=min(25, len(data)), alternating_row_color='teal', enable_events=False), sg.Button('Append Spreadsheet', key='-Append_csv-', font=font)],  # teal, lightblue
                ]
                window_data = sg.Window('output_'+day+'-'+month+'.csv', layout_data)
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
                        [sg.Table(values=data_input, headings=header_list_input, display_row_numbers=False, auto_size_columns=False,
                                  num_rows=min(25, len(data_input)), alternating_row_color='RoyalBlue')]  # teal, lightblue
                    ]
                    window_data_input = sg.Window('Your csv data displayed', layout_data_input)
                    event, values = window_data_input.read()
        if event == '-Append_csv-':
            sg.popup('THIS WORKS')  # LO here to try and enable events and delete rows if needed. 17/09/21

# plotting the data (not ready yet)
    if event == 'Analyse Data':
        empty_data = []
        empty_heading = []
        analysis_layout = [
            [sg.Text('Select a csv of your data:',  font=font, size=(20, 0)), sg.FileBrowse(key='csv_file2')],
            [sg.Text('Select type of analysis', font=font, size=(20, 0)), sg.Combo(
                ['Growth Curve', 'Stand Alone Titre Comparison', 'Calculate Median Culture', 'Mutation Rates'], key='analysis_type', size=(25, 1), font=font)],
            [sg.Submit('Select Analysis', font=font)],
            [sg.Text('_'*80)],
            [sg.Text('how many cultures do you have?', key='-Cultures Text-', font=font, visible=False), sg.Combo(list(range(1, 11)), key='-Cultures Dropdown-', font=font, visible=False)]
        ]
        window_analysis_question = sg.Window('Analysis', analysis_layout)
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
                    analysis_table_layout = [
                        [sg.Text('Select the rows to calculate the median from:')],
                        [sg.Table(values=data_input2, headings=headings2, key='-Median Table-', font=font, display_row_numbers=True, auto_size_columns=False,
                                  num_rows=min(10, len(data_input2)), alternating_row_color='RoyalBlue', visible=True,
                                  enable_events=False)],
                        [sg.Text('Strain 1:', key='strain1', visible=True, font=font), sg.InputText(key='Median_strain1', size=(10, 0), font=font, visible=True)],
                        [sg.Text('Strain 2:', key='strain2', visible=True, font=font), sg.InputText(key='Median_strain2', size=(10, 0), font=font, visible=True)],

                        [sg.Text('Strain 1 row start', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-1start-', font=font), sg.Text('Strain 1 row stop', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-1stop-', font=font),
                         sg.Text('Strain 2 row start', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-2start-', font=font), sg.Text('Strain 2 row stop', font=font), sg.Combo(list(range(0, len(data_input2)+1, 1)), key='-2stop-', font=font)],


                        [sg.Submit('Calculate', font=font), sg.Exit('Close', font=font, button_color='firebrick')],

                        [sg.Text('', key='strain1_median_culture', font=font, visible=False), sg.Text('', key='strain1_median_titre', font=font, visible=False)],
                        [sg.Text('', key='strain2_median_culture', font=font, visible=False), sg.Text('', key='strain2_median_titre', font=font, visible=False)],

                        # output of concat dfs showing median
                        [sg.Table(values=data_input2, headings=median_heading, key='-Median output-', font=font, display_row_numbers=False, num_rows=4, auto_size_columns=False, background_color='green', visible=False,
                                  enable_events=False),
                         sg.Button('Add to CSV', key='AddButton', visible=False)]

                    ]
                    window_median_table = sg.Window('Median Calculation', analysis_table_layout)
                    window_analysis_question.close()
                    while True:
                        event, values = window_median_table.read()
                        if event == 'Calculate':
                            try:
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
                                # print(median_culture1)
                                # print(median_culture2)

                                # concatenate the two dfs to show only one table
                                median_concat = pd.concat([median_culture1, median_culture2], axis=0, ignore_index=True)
                            #
                                median_list = median_concat.values.tolist()
                                # median1_heading = temp_df1.columns.tolist() # trouble updating the headings
                                # median2_heading = temp_df2.columns.tolist()

                            # appending the table to show the median cultures
                            # show the button to update the spreadhseet
                                window_median_table['-Median output-'].Update(values=median_list, visible=True)
                                window_median_table['AddButton'].Update(visible=True)

                                sg.popup('Now make a note of the median cultures', font=font)
                            except:
                                sg.popup('Enter row numbers first', font=font)

                        if event == 'AddButton':
                            try:
                                CSV_FILE = ('output_'+day+'-'+month+'.csv')
                                CSV_DF = pd.read_csv(CSV_FILE)
                                # use median_list to search df for indexes
                                indexes = []
                                cult1_strain = median_culture1['names'].to_list()
                                cult2_strain = median_culture2['names'].to_list()
                                joined_cult = cult1_strain + cult2_strain
                        # Retreiving the cultures that are the median values
                                for strain1 in joined_cult:
                                    if strain1 in CSV_DF.values:
                                        indices1 = str(CSV_DF[CSV_DF['Strain'] == strain1].index.values)
                                        if indices1 not in indexes:
                                            indexes.append(indices1)
                                    else:
                                        sg.popup('YOU DIED on culture 1')

                                if 'Median' not in CSV_DF.columns:  # LO here trying to add more than two cultures
                                    CSV_DF['Median'] = 'NA'
                                else:
                                    continue
                                for strain in joined_cult:
                                    CSV_DF.loc[CSV_DF.Strain == strain, 'Median'] = 'True'
                                CSV_DF.to_csv('UPDATED_output'+'_'+day+'-'+month+'.csv')
                                sg.popup('Data has been added!', font=font)
                            except:
                                sg.popup('YOU DIED earlier')

                        if event == sg.WIN_CLOSED or event == 'Close':
                            break
                    window_median_table.close()
                    continue
                    # save the selected rows into a df
                    # new_data1 = values['-Median Table-']
                    # closing and exiting the median window

                if values['analysis_type'] == 'Mutation Rates':
                    window_analysis_question.close()
                    sg.popup('NOTE: You must use the 1998 HTML program \nin conjunction which this data entry app', font=font)
                    try:
                        master_df = pd.read_csv(values['csv_file2'])
                        # master_df
                        headings2 = list(master_df.columns)
                        data_input2 = master_df.values.tolist()
                        data_strain = master_df.Strain.tolist()
                        data_titre = master_df.Titre.tolist()

                        median_heading = ['Culture', 'Titre']
                    except:
                        sg.popup('No file selected', font=font)
                        continue
                    mutation_layout_text = [
                        [sg.Text('Specify your parameters below:', font=font)],
                        [sg.Text('_'*20)],  # divider
                        [sg.Text('Median Culture Name:', font=font)],
                        [sg.Text('Antibiotic Used:', font=font)],
                        [sg.Text('Mutation Rate Calculation:')],
                        [sg.Button('Retrive Strains')],
                        [sg.Text('_'*20)],
                        [sg.Text('Number of Cultures (N):', font=font)],
                        [sg.Text('Cell Count per Culture (n):', font=font)],
                        [sg.Text('Mutation Events per Culture (r\N{SUBSCRIPT ZERO}):', font=font)],
                        [sg.Text('Mutation Rate (\u03BC):', font=font)],
                        [sg.Text('Mutation Rate (m):', font=font)],
                        [sg.Text('Sigma Value:', font=font)],
                        [sg.Text('Sigma / m:', font=font)],
                        [sg.Text('m / n:', font=font)],
                        [sg.Text('Sigma / n:', font=font)]
                    ]

                    mutation_layout_input = [
                        [sg.Text(' '*20)],
                        [sg.InputText(key='-Median_culture1-', size=(10, 1), font=font)],
                        [sg.InputText(key='-Ab-', size=(10, 1), font=font)],
                        [sg.Combo(['Method 1 (Drake): \u03BC = m / Nt', 'Method 2: \u03BC = m / (Nt-1)', 'Method 3: \u03BC = m / 2Nt',
                                  'Method 4: \u03BC = m ln(2) / Nt'], key='-Mrate_method-', enable_events=True)],
                        [sg.Text(' '*20)],
                        [sg.Text(' '*20)],
                        [sg.InputText(key='-Cultures-', size=(20, 1), font=font)],
                        [sg.InputText(key='-Cells-', size=(20, 1), font=font)],
                        [sg.InputText(key='-Mutations-', size=(20, 1), font=font)],
                        [sg.InputText(key='-Mrates-', size=(20, 1), font=font)],
                        [sg.InputText(key='-Mrates_m-', size=(20, 1), font=font)],
                        [sg.InputText(key='-Sigma-', size=(20, 1), font=font)],
                        [sg.InputText(key='-s/m-', size=(20, 1), font=font)],
                        [sg.InputText(key='-m/n-', size=(20, 1), font=font)],
                        [sg.InputText(key='-s/n-', size=(20, 1), font=font)]
                    ]

                    mutation_layout = [
                        [[sg.Column(mutation_layout_text),
                         sg.Column(mutation_layout_input, pad=((0, 0), (40, 0)))],
                         [sg.Button('Save Mutation Data', font=font), sg.Exit(font=font, button_color='firebrick', size=(10, 1), pad=((210, 0), (0, 0)))]
                         ]]

                    mutation_window = sg.Window('Mutation Rates', mutation_layout)
                    while True:
                        event, values = mutation_window.read()
                        if event == sg.WIN_CLOSED or event == 'Exit':
                            mutation_window.close()
                            break
                        if event == 'Retrive Strains':
                            try:
                                found_strain1 = master_df.loc[master_df['Strain'] == values['-Median_culture1-']]
                            # cleaning the dataframe to get our median with 100uL plated
                                true_medianstrain1 = found_strain1[found_strain1.Volume == 0.1]

                                LB_strain1 = true_medianstrain1[true_medianstrain1.Condition == 'LB']
                                Ab_strain1 = true_medianstrain1[true_medianstrain1.Condition == values['-Ab-']]

                                LB_total_cells1 = LB_strain1.Titre*5
                                Ab_total_cells1 = Ab_strain1.Titre*5

                        # Calculations for mutation rates, all slightly different
                                Mrates_classic = Ab_total_cells1.item() / LB_total_cells1.item()
                                # print(Mrates_classic)
                                #m = np.log(Mrates)

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

                        # Update the input fields showing the number of cells
                        # .item() retrieved the actual value
                                mutation_window['-Cells-'].Update(LB_total_cells1.item())
                                mutation_window['-Mutations-'].Update(Ab_total_cells1.item())
                                mutation_window['-Mrates-'].Update(Mrates)
                            except:
                                sg.popup('No such strain found')

                        if event == 'Save Mutation Data':
                            popup2 = sg.popup_yes_no('Do you want to append an existing file?')
                            mutation_dict = {'Cultures': [values['-Cultures-']],
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
                                except:
                                    sg.popup('You died...')
                            if popup2 == 'Yes':
                                browse_file_layout = [
                                    [sg.Text('Select your csv file:'), sg.FileBrowse(key='csv_file')],
                                    [sg.Submit(key='csv_submit')]
                                ]
                                browse_csv_window = sg.Window('Find the csv file to display', browse_file_layout)
                                event, values = browse_csv_window.read()
                                if event == 'csv_submit':
                                    CSV_FILE_input = values['csv_file']
                                    df1 = pd.read_csv(CSV_FILE_input)
                                    mutation_dataframe = pd.DataFrame(mutation_dict)
                                    df1 = df1.append(mutation_dataframe, ignore_index=True)
                                    df1.to_csv((CSV_FILE_input), index=False)
                                    sg.popup('Data saved!')
                                    browse_csv_window.close()
                                    continue
# left off here trying to append the csv to get an update mutation rate df which is just copied from the 1998 html prog.
                            # clear_input()
window.close()


##########################################################################################
#
#                                         TEST SPACE
#
##########################################################################################


# trying to get a plotter page in the app to show possible VT comparison, this is not essential as can be done in R easily.
''' # plotting the data - work this out later
plt.scatter(data_temp1.names, data_temp1.titre, color='RoyalBlue')
plt.xlabel('Culture')
plt.ylabel('Cells/mL')
plt.title('SLM1043 Cultures')
plt.xticks(rotation=75)'''

# manual calculations
iter = 1e-8
N = 9
n = 1272727272.7272723
m = 10818.18181818182
u = 8.500000000000005e-6

# trying out a while loop that takes into account the iterations
m0 = 0.0
r0 = m
while (np.abs(m0 - m) >= iter):
    m0 = m
    divident = (1.24 * m0) + (m0 * np.log(m0)) - r0
    divisor = 2.24 + np.log(m0)
    u = m0 - (divident / divisor)
    print(u)  # mutation rate is not the same as in the html program

# sigma value
divident_s = 12.7
divisor_s = (2.24 + np.log(m)) * (2.24 + np.log(m))
s = m * np.sqrt((1/N) * (divident_s/divisor_s))
s

dict = {'col1': [1], 'col2': [3]}
mutation_dataframe = pd.DataFrame(dict)
mutation_dataframe


# mutationrate from the 1998 program
1.288e3
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


# append dataframe with new column
CSV_FILE = ('output_'+day+'-'+month+'.csv')
CSV_DF = pd.read_csv(CSV_FILE)
xlist = ['DG011 #5', 'DG011 #6', 'DG012 #5']
test_df = CSV_DF
test_df['Median'] = 'NA'
test_df
for strain in xlist:
    test_df.loc[test_df.Strain == strain, 'Median'] = 'True'

test_df
