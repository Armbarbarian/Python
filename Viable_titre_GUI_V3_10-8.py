# working from example https://www.python-course.eu/tkinter_entry_widgets.php

# testing out how to build viable titre GUI for lab work
from tkinter import *

# set the root function to build the window
root = Tk()
# give the window a title
root.title('Viable Titre ')
# dimensions of the window, can change at will
root.geometry('500x300')

# condition of the plate
Label(root, text='Enter the plate condition:').grid(row=0)
strain_input = Entry(root, width=35, borderwidth=5)
strain_input.grid(row=0, column=1)

# strain name
Label(root, text='Enter your Strain:').grid(row=1)
strain_input = Entry(root, width=35, borderwidth=5)
strain_input.grid(row=1, column=1)

# dilution
Label(root, text='Enter the dilution:').grid(row=2)
dil_input = Entry(root, width=35, borderwidth=5)
dil_input.grid(row=2, column=1)

# volume plated
Label(root, text='Enter the volume plated:').grid(row=3)
vol_input = Entry(root, width=35, borderwidth=5)
vol_input.grid(row=3, column=1)

# colony number
Label(root, text='Number of Colonies A:').grid(row=4)
# input from user for the strain name
col_inputA = Entry(root, width=35, borderwidth=5)
col_inputA.grid(row=4, column=1)
Label(root, text='Number of Colonies B:').grid(row=5)
# input from user for the strain name
col_inputB = Entry(root, width=35, borderwidth=5)
col_inputB.grid(row=5, column=1)

# calculation from input


def get_calculation():
    calculation_label.config(text=((int(col_inputA.get()) + int(col_inputB.get())
                                    ) / 2) / (float(vol_input.get()) * float(dil_input.get())))


calculate = Button(root, text='Calculate Viable Titre',
                   padx=50, pady=25, command=get_calculation)
calculate.grid(row=6, column=0)

calculation_label = Label(root, text='')
calculation_label.grid(row=7, column=0)

# save the viable titre following calculation


# call the window up
root.mainloop()
