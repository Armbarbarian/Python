# making a viable titre gui using tkinter
from tkinter import *

root = Tk()

# user input entry
input = Entry(root, width=50, borderwidth=5)
input.pack()
input.insert(0, 'Enter your name: ')

# tell the button to do something by defining a function


def myClick():
    hello = 'Hello ' + input.get()
    myLabel = Label(root, text=hello)
    myLabel.pack()


# add a button
# padx and pady define the size of the button
# state=DISABLED if we want the button to be greyed out
myButton1 = Button(root, text='GO!', padx=50,
                   pady=25, command=myClick, fg='blue', bg='white')

# shove on screen
myButton1.pack()


#  main loop to show it on scree
root.mainloop()
