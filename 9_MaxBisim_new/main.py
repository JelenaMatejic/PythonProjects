# from curses import window
from fileinput import filename
from turtle import color
# from matplotlib.pyplot import text
from nerode import NerodovaKonstrukcija
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from multiprocessing.sharedctypes import Value

# Default vrednosti
file_name = ""
nk = NerodovaKonstrukcija()

# Odabir input fajla
def openfile_A():
    selected_file = filedialog.askopenfilename()
    label_file.config(bg="SystemButtonFace")
    label_file.config(fg="black")  
    # file_name = selected_file.split('/')[len(selected_file.split('/'))-1]
    label_file['text'] = selected_file
    return selected_file

def openfile_B():
    selected_file = filedialog.askopenfilename()
    label_file_2.config(bg="SystemButtonFace")
    label_file_2.config(fg="black")  
    # file_name = selected_file.split('/')[len(selected_file.split('/'))-1]
    label_file_2['text'] = selected_file
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

# Provera da li je unet parametar n ili e
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

# Promeniti natpise u labelama iznad polja za ispis
def setLabels(type):
    label_initial['text'] = "Initial"
    param = input_parameter.get()
    if type == 'Word length':
        label_output_1['text'] = "Sigma Vectors - Word Length n = " + param
        label_output_2['text'] = "Tau Vectors - Word Length n = " + param
    elif type == 'Threshold (decimal)' or type == 'Threshold (fraction)':
        label_output_1['text'] = "Sigma Vectors - Threshold e = " + param
        label_output_2['text'] = "Tau Vectors - Threshold e = " + param
    elif type == 'Bisimulation':
        label_output_1['text'] = "Tau Vectors With Bound e = " + param
        label_output_2['text'] = "Maximal Bisimulation"
    elif type == 'Bisimulation 2':
        label_output_1['text'] = "Bisimulations e = " + param
        label_output_2['text'] = "Maximal Bisimulation"

# U zavisnosti od toga koja je opcija selektovana treba da stoji e ili n
def on_field_change(index, value, op):
    if select_type.get() == "Word length":
        label_parameter['text'] = "n = "
    else:
        label_parameter['text'] = "e = "

# Računanje izlaznih rešenja
def calculate():
    if checkFile() and checkSelectParam() and checkInputParam() :
        nk = NerodovaKonstrukcija()
        file_name = label_file['text']
        type_name = select_type.get()
        setLabels(type_name)

        file_name_2 = label_file_2['text']
        type_name_2 = select_type.get()
        setLabels(type_name_2)

        # Kada pozivamo funkciju za izračunavanje nerode() ona kao parametre očekuje fajl, tip računanja koje želimo, dužinu reči, epsilom
        # Dužinu reči je potrebno proslediti samo ukoliko želimo da se algoritam izvršava do određene dužine reči, u suprotnom kao dužinu prosleđujemo -1
        # Kada računamo do dužine reči, tada nemamo epsilon i onda umesto njega prosleđujemo 0
        e = float(input_parameter.get())
        n = -1
        if type_name == "Word length":
            e = 0
            flag = True
            try:
                int(input_parameter.get())
            except ValueError:
                flag = False
            
            if flag:
                label_parameter['text'] = "n = "
                n = int(input_parameter.get())
            else:
                label_parameter['text'] = "n should be integer "

        res = nk.nerode(file_name, file_name_2, type_name, n, e) # kao rezultat vraća dva stringa koji su rezultat izračunavanja i ispisujemo ih na ekranu
        printOnScreen(text_box_initial, nk.print_initial_in_GUI())
        printOnScreen(text_box_output_1, res[0])
        printOnScreen(text_box_output_2, res[1])

# Kreiranje prozora
window = tk.Tk()
window.geometry("1220x400") # zadavanje dimenzija prozoru
window.title("Nerodova konstrukcija") # naslov u prozoru
# Odabir fajla 1
btn_file = tk.Button(window, text="Open File 1", command=openfile_A, width = 20)
btn_file.grid(column=1, row=1)
label_file = tk.Label(text='Please choose a file for automaton A')
label_file.grid(column=2, row=1, columnspan=2)
# Odabir fajla 2
btn_file_2 = tk.Button(window, text="Open File 2", command=openfile_B, width = 20)
btn_file_2.grid(column=1, row=2)
label_file_2 = tk.Label(text='Please choose a file for automaton B')
label_file_2.grid(column=2, row=2, columnspan=2)
# Odabir parametra
label_parameter = tk.Label(window, text='') # za sada je labela prazna, a u zavisnosti od odabira stajaće n (dužina reči) ili e (threshold)
label_parameter.grid(column=2, row=3)
input_parameter = tk.Entry(window, width=45)
input_parameter.grid(column=3, row=3)
# Računanje
btn_calculate = tk.Button(window, text="Calculate", command=calculate, width = 30, height=3)
btn_calculate.grid(column=4, row=1, rowspan=4)
# Labela i Text area polje za prikaz početnog automata
label_initial = tk.Label(text='Initial')
label_initial.grid(column=1, row=4)
text_box_initial = Text(window, width = 30, height = 70, spacing1 = 2)
text_box_initial.grid(column=1, row=5)
# Labela i Text area polje za prikaz automata bez ograničenja e
label_output_1 = tk.Label(text='')
label_output_1.grid(column=2, row=4, columnspan=2)
text_box_output_1 = Text(window, width = 70, height = 70, spacing1 = 2)
text_box_output_1.grid(column=2, row=5, columnspan=2)
# Labela i Text area polje za prikaz automata sa ograničenjem e
label_output_2 = tk.Label(text='')
label_output_2.grid(column=4, row=4)
text_box_output_2 = Text(window, width = 70, height = 70, spacing1 = 2)
text_box_output_2.grid(column=4, row=5)
# Odabir strukture
v = StringVar()
v.trace('w',on_field_change) # kada se odabir promeni, treba da stoji n (dužina reči) ili e (threshold)
select_type= ttk.Combobox(window, textvar=v, justify='center', width = 20, state='readonly')
select_type.set('Choose type')      
select_type['values'] = ('Word length', 'Threshold (decimal)', 'Threshold (fraction)', 'Bisimulation', 'Bisimulation 2')
select_type.grid(column=1, row=3)
# Pokretanje prozora za prikaz GUI
window.mainloop() 