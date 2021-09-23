# testing out how to build viable titre GUI for lab work
from tkinter import *

# set the root function to build the window
root = Tk()
# give the window a title
root.title('Viable Titre ')
# dimensions of the window, can change at will
root.geometry('500x300')

# give each entry widget a title so the user knows what to input.
Label(root, text='Enter your Strain').grid(row=0)
# input from user for the strain name
strain_input = Entry(root, width=35, borderwidth=5)
strain_input.grid(row=0, column=1)

# strain_input.insert(0, 'Enter your Strain: ') #for pre-defined entry

# dilution list drop down menu
dilutions_list = ['10e-1', '10e-2', '10e-3', '10e-4', '10e-5', '10e-6', '10e-7', '10e-8']
dilutions = StringVar(root)
dilutions.set('Select a Dilution')

dil1 = OptionMenu(root, dilutions, *dilutions_list)
dil1.config(width=20, font=('Calibri', 14))
dil1.grid(row=1, column=0)


# Colonies list drop down menu

colonies_list = [i for i in range(100)]
colonies_list
colonies = StringVar(root)
colonies.set('Select the Colony Number')

opt2 = OptionMenu(root, colonies, *colonies_list)
opt2.config(width=20, font=('Calibri', 14))
opt2.grid(row=2, column=0)

# call the window up
root.mainloop()
