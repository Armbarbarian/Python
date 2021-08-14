import PySimpleGUI as sg
from random import randint as rand

def table_example():
    data = [list(str(rand(0,50)) for i in range(5)) for i in range(10)]
    header_list = ['C1', 'C2', 'C3', 'C4', 'C5']
    layout = [[sg.Table(values=data,
                        headings=header_list,
                        auto_size_columns=True,
                        justification='center',
                        num_rows=min(len(data), 20),
                        alternating_row_color='lightblue',
                        row_colors=((0, 'red'), (2, 'yellow')),
                        display_row_numbers=True,
                        key='table')],
              [sg.Button('Randomize'), sg.Button('Close')]]

    window = sg.Window('table', layout)
    while True:
        event, values = window.Read()
        if event in ('Close', None): break
        if event is 'Randomize':
            window.Element('table').Update(values=[list(str(rand(0,50)) for i in range(5)) for i in range(10)],
                                           num_rows=min(len(data), 20))

table_example()
