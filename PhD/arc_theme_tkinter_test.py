from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk

window = ThemedTk(theme="black")
ttk.Button(window, text="Quit", command=window.destroy).pack()

s = ttk.Style()
s.configure('Wild.TButton',
            background='black',
            foreground='white',
            highlightthickness='20',
            font=('Helvetica', 18, 'bold'))
s.map('Wild.TButton',
      foreground=[('disabled', 'yellow'),
                  ('pressed', 'red'),
                  ('active', 'blue')],
      background=[('disabled', 'magenta'),
                  ('pressed', '!focus', 'cyan'),
                  ('active', 'green')],
      highlightcolor=[('focus', 'green'),
                      ('!focus', 'red')],
      relief=[('pressed', 'groove'),
              ('!pressed', 'ridge')])

window.mainloop()
