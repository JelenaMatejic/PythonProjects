from curses import window
from fileinput import filename

from matplotlib.pyplot import text
from nerode import NerodovaKonstrukcija
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import graph
import os

# Default vrednosti
file_name = ""
selected_file = ""
nk = NerodovaKonstrukcija()

# Odabir input fajla
def openfile():
    selected_file = filedialog.askopenfilename()
    label_file.config(bg="SystemButtonFace")
    label_file.config(fg="black")  
    file_name = selected_file.split('/')[len(selected_file.split('/'))-1]
    label_file['text'] = file_name
    return selected_file

# Provera da li je odabran fajl
def check():
    file_name = label_file['text']
    if file_name == "" or file_name == "Please choose a file":
        label_file['text'] = "Please choose a file"
        label_file.config(bg="yellow")
        label_file.config(fg="red")   
        return False
    return True

# Nerodova konstrukcija
def calculate():
    if check():
        file_name = label_file['text']
        nk.nerode(file_name)
        btn_non_determ["state"] = "normal"
        btn_determ["state"] = "normal"
        text_box_nondeterm.insert(END, nk.print_non_determ_results_in_GUI())
        text_box_determ.insert(END, nk.print_determ_results_in_GUI())
        # graph.plot_graphs(nk)

# Prikaz nedeterminističkog automata
def show_non_determ():
    if check():
        graph.plot_non_determ(nk)

# Prikaz determinističkog automata
def show_determ():
    if check():
        graph.plot_determ(nk)

# Kreiranje prozora
window = tk.Tk()
window.geometry("400x400") # zadavanje dimenzija prozoru
window.title("Nerodova konstrukcija") # naslov u prozoru

# Odabir fajla
btn_file = tk.Button(window, text="Open File", command=openfile, width = 17)
btn_file.grid(column=1, row=1)
label_file = tk.Label(text='Please choose a file')
label_file.grid(column=2, row=1)
# Odabir strukture
select_structure = ttk.Combobox(window, justify='center', width = 17)
select_structure.set('Product Structure')
select_structure.grid(column=1, row=2)
# Računanje
btn_calculate = tk.Button(window, text="Calculate", command=calculate, width = 17)
btn_calculate.grid(column=2, row=2)
# Prikaz nedeterminističkog automata
btn_non_determ = tk.Button(window, text="Non deterministic", command=show_non_determ, width = 17, state="disabled")
btn_non_determ.grid(column=1, row=3)
# Prikaz determinističkog automata
btn_determ = tk.Button(window, text="Deterministic", command=show_determ, width = 17, state="disabled")
btn_determ.grid(column=2, row=3)
# Text area polje za prikaz nedeterminističkog automata
text_box_nondeterm = Text(window, width = 27, height = 20, spacing1 = 2)
text_box_nondeterm.grid(column=1, row=4)
# Text area polje za prikaz determinizacije automata
text_box_determ = Text(window, width = 27, height = 20, spacing1 = 2)
text_box_determ.grid(column=2, row=4)
# Pokretanje prozora za prikaz GUI
window.mainloop() 