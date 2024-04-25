# working from example https://www.python-course.eu/tkinter_entry_widgets.php

# testing out how to build viable titre GUI for lab work
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd
import numpy as np

# set the root function to build the window
root = ThemedTk(theme='Adapta')

# give the window a title
root.title('Viable Titre')
# dimensions of the window, can change at will
# root.geometry('500x300')


# __________________________________________________________________________________________ Strain 1

# condition of the plate
ttk.Label(root, text='Enter the plate condition:', font=("Calibri", 14)).grid(row=0)
cond_input = ttk.Entry(root, width=10)
cond_input.grid(row=0, column=1)
cond_input.config(font=("Calibri", 14))

# strain name
ttk.Label(root, text='Enter your Strain:', font=("Calibri", 14)).grid(row=1)
strain_input = ttk.Entry(root, width=10)
strain_input.grid(row=1, column=1)
strain_input.config(font=("Calibri", 14))

# dilution
ttk.Label(root, text='Enter the first dilution:', font=("Calibri", 14)).grid(row=2)
dilutions_list1 = ['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8']
dilutions1 = StringVar(root)
dilutions1.set('Select a Dilution')
dil1 = ttk.OptionMenu(root, dilutions1, '', *dilutions_list1)
dil1.grid(row=2, column=1)

ttk.Label(root, text='Enter the second dilution:', font=("Calibri", 14)).grid(row=3)
dilutions_list2 = ['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8']
dilutions2 = StringVar(root)
dilutions2.set('Select a Dilution')
dil2 = ttk.OptionMenu(root, dilutions2, '', *dilutions_list2)
dil2.grid(row=3, column=1)


# volume plated
# for spot dilution is always 10uL
# for whole plate is always 100uL
ttk.Label(root, text='Enter the volume plated (mL):', font=("Calibri", 14)).grid(row=4)
vol_input = ttk.Entry(root, width=10)
vol_input.grid(row=4, column=1)
vol_input.config(font=("Calibri", 14))

# colony number
ttk.Label(root, text='Number of Colonies (1st Dil.):', font=("Calibri", 14)).grid(row=5)
col_input1A = ttk.Entry(root, width=10)
col_input1A.grid(row=5, column=1)
col_input1A.config(font=("Calibri", 14))
col_input2A = ttk.Entry(root, width=10)
col_input2A.grid(row=5, column=2)
col_input2A.config(font=("Calibri", 14))

ttk.Label(root, text='Number of Colonies (2nd Dil.):', font=("Calibri", 14)).grid(row=6)
col_input1B = ttk.Entry(root, width=10)
col_input1B.grid(row=6, column=1)
col_input1B.config(font=("Calibri", 14))
col_input2B = ttk.Entry(root, width=10)
col_input2B.grid(row=6, column=2)
col_input2B.config(font=("Calibri", 14))

# calculation from input


def get_calculation():
    averageA = (int(col_input1A.get()) + int(col_input2A.get()))/2
    averageB = (int(col_input1B.get()) + int(col_input2B.get()))/2
    calculation_label.config(
        text=((averageA+averageB) / (float(vol_input.get()) * (float(dilutions1.get())+float(dilutions2.get())))))


calculate = ttk.Button(root, text='Calculate Viable Titre (cells/mL)',
                       command=get_calculation, cursor='pencil')
calculate.grid(row=7, column=0)


calculation_label = Label(root, text=(''))
calculation_label.grid(row=8, column=0)
calculation_label.config(font=("Calibri", 14))


# save the viable titre following calculation
# https://stackoverflow.com/questions/44798950/how-to-display-a-dataframe-in-tkinter
update_button1 = ttk.Button(root, text='Update spreadsheet',
                            state='disable')  # to do: update_df command
update_button2 = ttk.Button(root, text='Update spreadsheet',
                            state='disable')  # to do: update_df command
update_button1.grid(row=7, column=1)
update_button2.grid(row=7, column=5)


# line separation between the two
ttk.Separator(root, orient=VERTICAL).grid(column=3, row=0, rowspan=10, sticky='ns')

# __________________________________________________________________________________________ Strain 2

# condition of the plate
ttk.Label(root, text='Enter the plate condition:', font=("Calibri", 14)).grid(row=0, column=4)
cond_input2 = ttk.Entry(root, width=10)
cond_input2.grid(row=0, column=5)
cond_input2.config(font=("Calibri", 14))

# strain name
ttk.Label(root, text='Enter your Strain:', font=("Calibri", 14)).grid(row=1, column=4)
strain2_input = ttk.Entry(root, width=10)
strain2_input.grid(row=1, column=5)
strain2_input.config(font=("Calibri", 14))

# dilution
ttk.Label(root, text='Enter the first dilution:', font=("Calibri", 14)).grid(row=2, column=4)
dilutions_list1_2 = ['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8']
dilutions1_2 = StringVar(root)
dilutions1_2.set('Select a Dilution')
dil1_2 = ttk.OptionMenu(root, dilutions1_2, '', *dilutions_list1_2)
dil1_2.grid(row=2, column=5)

ttk.Label(root, text='Enter the second dilution:', font=("Calibri", 14)).grid(row=3, column=4)
dilutions_list2_2 = ['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8']
dilutions2_2 = StringVar(root)
dilutions2_2.set('Select a Dilution')
dil2_2 = ttk.OptionMenu(root, dilutions2_2, '', *dilutions_list2_2)
dil2_2.grid(row=3, column=5)


# volume plated
# for spot dilution is always 10uL
# for whole plate is always 100uL
ttk.Label(root, text='Enter the volume plated (mL):', font=("Calibri", 14)).grid(row=4, column=4)
vol_input_2 = ttk.Entry(root, width=10)
vol_input_2.grid(row=4, column=5)
vol_input_2.config(font=("Calibri", 14))

# colony number
ttk.Label(root, text='Number of Colonies (1st Dil.):', font=("Calibri", 14)).grid(row=5, column=4)
col_input1A_2 = ttk.Entry(root, width=10)
col_input1A_2.grid(row=5, column=5)
col_input1A_2.config(font=("Calibri", 14))
col_input2A_2 = ttk.Entry(root, width=10)
col_input2A_2.grid(row=5, column=6)
col_input2A_2.config(font=("Calibri", 14))

ttk.Label(root, text='Number of Colonies (2nd Dil.):', font=("Calibri", 14)).grid(row=6, column=4)
col_input1B_2 = ttk.Entry(root, width=10)
col_input1B_2.grid(row=6, column=5)
col_input1B_2.config(font=("Calibri", 14))
col_input2B_2 = ttk.Entry(root, width=10)
col_input2B_2.grid(row=6, column=6)
col_input2B_2.config(font=("Calibri", 14))

# calculation from input


def get_calculation_2():
    averageA_2 = (int(col_input1A_2.get()) + int(col_input2A_2.get()))/2
    averageB_2 = (int(col_input1B_2.get()) + int(col_input2B_2.get()))/2
    calculation_label_2.config(
        text=((averageA_2+averageB_2) / (float(vol_input_2.get()) * (float(dilutions1_2.get())+float(dilutions2_2.get())))))


calculate_2 = ttk.Button(root, text='Calculate Viable Titre (cells/mL)',
                         command=get_calculation_2, cursor='pencil')
calculate_2.grid(row=7, column=4)


calculation_label_2 = Label(root, text=(''))
calculation_label_2.grid(row=8, column=4)
calculation_label_2.config(font=("Calibri", 14))

# Show a table output
'''frame = Frame(root)
frame.grid(row=8, column=1)
df = ttk.Treeview(frame, show='headings', height=5)
df.grid(row=11)

df.heading(text='Condition')
df.heading(text='Strain')
df.heading(text='Dilution')
df.heading(text='Av. Colonies')
df.heading(text='Viable Titre')'''


# call the window up
root.mainloop()
