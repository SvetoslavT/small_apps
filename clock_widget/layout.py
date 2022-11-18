
from tkinter import *
from tkinter.ttk import *
from time import strftime

root = Tk()
root.title('Live_clock')

def time():
	string = strftime('%H:%M:%S %p')
	lbl.config(text = string)
	lbl.after(1000, time)


lbl = Label(root, font = ('calibri', 40, 'bold'),
			background = 'gray',
			foreground = 'white')


lbl.pack(anchor = 'center')
time()

mainloop()
