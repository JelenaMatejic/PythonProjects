from curses import window
from fileinput import filename
from matplotlib.pyplot import text
from nerode import NerodovaKonstrukcija
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk

# Default vrednosti
file_name = ""
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
        text_box_initial.insert(END, nk.print_initial_in_GUI())
        text_box_non_bounded.insert(END, nk.print_results_in_GUI())
        text_box_bounded.insert(END, nk.print_bounded_results_in_GUI())

# Kreiranje prozora
window = tk.Tk()
window.geometry("1220x400") # zadavanje dimenzija prozoru
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
# Labela i Text area polje za prikaz početnog automata
label_initial = tk.Label(text='Initial')
label_initial.grid(column=1, row=3)
text_box_initial = Text(window, width = 30, height = 20, spacing1 = 2)
text_box_initial.grid(column=1, row=4)
# Labela i Text area polje za prikaz automata bez ograničenja e
label_without = tk.Label(text='Without bound')
label_without.grid(column=2, row=3)
text_box_non_bounded = Text(window, width = 70, height = 20, spacing1 = 2)
text_box_non_bounded.grid(column=2, row=4)
# Labela i Text area polje za prikaz automata sa ograničenjem e
label_with = tk.Label(text='With a bound')
label_with.grid(column=3, row=3)
text_box_bounded = Text(window, width = 70, height = 20, spacing1 = 2)
text_box_bounded.grid(column=3, row=4)
# Pokretanje prozora za prikaz GUI
window.mainloop() 