import tkinter as tk
from time import strftime

def time():
    string = strftime('%H:%M:%S %p')
    label.config(text=string)
    label.after(1000, time)

root = tk.Tk()
root.title("Today's Clock")
root.geometry('600x300')
root.configure(background='purple')

label = tk.Label(root, font=('calibri', 40, 'bold'), background='navy blue', foreground='white')
label.pack(anchor='center')

time()

root.mainloop()