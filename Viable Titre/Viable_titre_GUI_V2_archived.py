# testing out how to build viable titre GUI for lab work
from tkinter import *

# set the root function to build the window
root = Tk()
# give the window a title
root.title('Viable Titre ')
# dimensions of the window, can change at will
root.geometry('500x300')

# give each entry widget a title so the user knows what to input.
Label(root, text='Enter your Strain:').grid(row=0)
strain_input = Entry(root, width=35, borderwidth=5)
strain_input.grid(row=0, column=1)

# dilution
Label(root, text='Enter the dilution:').grid(row=1)
dil_input = Entry(root, width=35, borderwidth=5)
dil_input.grid(row=1, column=1)

# colony number
Label(root, text='Number of Colonies:').grid(row=2)
# input from user for the strain name
col_input = Entry(root, width=35, borderwidth=5)
col_input.grid(row=2, column=1)

# calculation from input


# call the window up
root.mainloop()
