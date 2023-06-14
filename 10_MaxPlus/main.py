from fileinput import filename
from turtle import color
from matplotlib.pyplot import text
from nerode import NerodovaKonstrukcija
import tkinter as tk
# from tkinter import *
from tkinter import END, Text, filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import emoji

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
def checkFile():
    file_name = label_file['text']
    if file_name == "" or file_name == "Please choose a file":
        label_file['text'] = "Please choose a file"
        label_file.config(bg="#268FFF")
        label_file.config(fg="white")   
        return False
    return True

# Provera da li je unet parametar n
def checkInputParam():
    input_param = input_parameter.get()
    if input_param == "":
        label_parameter.config(bg="#268FFF")
        label_parameter.config(fg="white")
        return False
    else:
        label_parameter.config(bg="SystemButtonFace")
        label_parameter.config(fg="black") 
        return True

# Provera da li je selektovan tip izračunavanja
def checkSelectParam():
    if select_type.get() == "Choose type":
        style= ttk.Style()
        style.configure("TCombobox", background= "yellow")
        return False
    return True

# Ispis izračunatih podataka na ekranu
def printOnScreen(field, value):
    field.configure(state="normal") # enable polje
    field.delete("0.0", 'end') # brisanje sadržaja iz polja
    field.insert(END, value) # ispis podataka u polje
    field.configure(state="disabled") # disable polje, da korisnik ne bi mogao da menja nešto u polju

# Računanje izlaznih rešenja
def calculate():
    if checkFile() and checkSelectParam() and checkInputParam() :
        nk = NerodovaKonstrukcija()
        file_name = label_file['text']
        type_name = select_type.get()
        n = int(input_parameter.get())
        res = nk.nerode(file_name, type_name, n, type_name) # kao rezultat vraća dva stringa koji su rezultat izračunavanja i ispisujemo ih na ekranu
        printOnScreen(text_box_initial, nk.print_initial_in_GUI())
        printOnScreen(text_box_output_1, res[0])
        printOnScreen(text_box_output_2, res[1])

# Kreiranje prozora
window = tk.Tk()
window.geometry("1220x400") # zadavanje dimenzija prozoru
window.title("Max-Plus") # naslov u prozoru
# Odabir fajla
btn_file = tk.Button(window, text="Open File", command=openfile, width = 20)
btn_file.grid(column=1, row=1)
label_file = tk.Label(text='Please choose a file')
label_file.grid(column=2, row=1, columnspan=2)
# Odabir parametra
label_parameter = tk.Label(window, text='n = ') # za sada je labela prazna, a u zavisnosti od odabira stajaće n (dužina reči) ili e (threshold)
label_parameter.grid(column=2, row=2)
input_parameter = tk.Entry(window, width=45)
input_parameter.grid(column=3, row=2)
# Računanje
btn_calculate = tk.Button(window, text="Calculate", command=calculate, width = 30, height=2)
btn_calculate.grid(column=4, row=1, rowspan=2)
# Labela i Text area polje za prikaz početnog automata
label_initial = tk.Label(text='Initial')
label_initial.grid(column=1, row=3)
text_box_initial = Text(window, width = 30, height = 70, spacing1 = 2)
text_box_initial.grid(column=1, row=4)
# Labela i Text area polje za prikaz automata bez ograničenja e
label_output_1 = tk.Label(text='Sigma vectors')
label_output_1.grid(column=2, row=3, columnspan=2)
text_box_output_1 = Text(window, width = 70, height = 70, spacing1 = 2)
text_box_output_1.grid(column=2, row=4, columnspan=2)
# Labela i Text area polje za prikaz automata sa ograničenjem e
label_output_2 = tk.Label(text='Tau vectors')
label_output_2.grid(column=4, row=3)
text_box_output_2 = Text(window, width = 70, height = 70, spacing1 = 2)
text_box_output_2.grid(column=4, row=4)
# Odabir strukture
select_type= ttk.Combobox(window, justify='center', width = 20, state='readonly')
select_type.set('Choose type')      
select_type['values'] = ('Rmax (decimal)', 'Rmax (fraction)', 'R' + emoji.emojize(':infinity:'))
select_type.grid(column=1, row=2)
# Pokretanje prozora za prikaz GUI
window.mainloop() 