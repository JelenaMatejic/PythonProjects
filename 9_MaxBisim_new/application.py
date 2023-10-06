from cmath import tau
from fileinput import filename
from turtle import color
from automaton import Automaton
from matrix import Matrix
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from multiprocessing.sharedctypes import Value
from tkinter import messagebox
import numpy as np
import utility


class Application:
    def __init__(self, root):
        # Default values
        self.selected_file_1 = ""
        self.selected_file_2 = ""

        # Create GUI elements
        self.root = root
        self.root.geometry("1220x400")  # Set window dimensions
        self.root.title("Nerodova konstrukcija")  # Set window title

        # Create GUI elements
        self.button_browse_1 = tk.Button(self.root, text="Browse File 1", command=self.browse_file_1)
        self.button_browse_1.grid(row=0, column=0, padx=10, pady=5)
        self.selected_file_label_1 = tk.Label(self.root, text="Selected File 1: ")
        self.selected_file_label_1.grid(row=0, column=1, padx=10, pady=5)

        self.button_browse_2 = tk.Button(self.root, text="Browse File 2", command=self.browse_file_2)
        self.button_browse_2.grid(row=1, column=0, padx=10, pady=5)
        self.selected_file_label_2 = tk.Label(self.root, text="Selected File 2: ")
        self.selected_file_label_2.grid(row=1, column=1, padx=10, pady=5)

       # Radio buttons for bisimulation type
        self.selected_radio = tk.StringVar()
        self.selected_radio.set("bisimulation")  # Set the default selection to "Bisimulation"

        radio_btn_autobisimulation = tk.Radiobutton(self.root, text="Autobisimulation", variable=self.selected_radio, value="autobisimulation")
        radio_btn_autobisimulation.grid(row=2, column=0, sticky='w')
        radio_btn_bisimulation = tk.Radiobutton(self.root, text="Bisimulation", variable=self.selected_radio, value="bisimulation")
        radio_btn_bisimulation.grid(row=3, column=0, sticky='w')

        # Input field for threshold value
        self.threshold_label = tk.Label(self.root, text="Threshold:")
        self.threshold_label.grid(row=4, column=0, padx=10, pady=5)
        self.threshold_entry = tk.Entry(self.root)
        self.threshold_entry.grid(row=4, column=1, padx=10, pady=5)

        # Computation button
        self.button_compute = tk.Button(self.root, text="Compute", command=self.compute)
        self.button_compute.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def browse_file_1(self):
        self.selected_file_1 = filedialog.askopenfilename()
        if self.selected_file_1:
            self.selected_file_label_1.config(text="Selected File 1: " + self.selected_file_1)

    def browse_file_2(self):
        self.selected_file_2 = filedialog.askopenfilename()
        if self.selected_file_2:
            self.selected_file_label_2.config(text="Selected File 2: " + self.selected_file_2)
    
    def compute(self):
        selected_option = self.selected_radio.get()
        threshold_value = self.threshold_entry.get()

        if not self.selected_file_1:
            messagebox.showinfo("Error", "Please choose File 1.")
        elif not self.selected_file_2:
            messagebox.showinfo("Error", "Please choose File 2.")
        elif not threshold_value.strip(): 
            messagebox.showinfo("Error", "Please input threshold")
        elif float(threshold_value)<0 or float(threshold_value)>1:
            messagebox.showinfo("Error", "Threshold must be a number >=0 and <=1")
        else:
            automaton1 = Automaton(self.selected_file_1)
            automaton2 = Automaton(self.selected_file_2)

            # Access the selected radio button value using self.selected_radio.get()
            if selected_option == "autobisimulation":
                t_arr = [automaton1.tau]
                max_bisim = self.bisim(automaton1.tau, automaton1.tau)
                max_bisim.print_matrix()
                
                for t in t_arr:
                    for d in automaton1.transitions:
                        t_d = utility.multiply(d, t.transpose(), float(threshold_value)) # row vectormatrix
                        t_d.name = t.name + d.name
                        t_d = t_d.transpose()

                        if(any(x.value == t_d.value for x in t_arr) != True):
                            t_arr.append(t_d)
                            max_bisim_tmp = self.bisim(t_d, t_d) # matrix 
                            max_bisim = utility.min_matrix(max_bisim, max_bisim_tmp)
                            max_bisim_tmp.print_matrix()
            else:
                t_w = ['t_'] # words array
                t_A = [{'word': 't_', 'vector': automaton1.tau}]
                t_B = [{'word': 't_', 'vector': automaton2.tau}]
                max_bisim = self.bisim(automaton1.tau, automaton2.tau)
                max_bisim.print_matrix()
                
                for w in t_w:
                    t1 = utility.findByKey(t_A, w) # vector in automaton A for selected word
                    t2 = utility.findByKey(t_B, w) # vector in automaton B for selected word

                    for d1, d2 in zip(automaton1.transitions, automaton2.transitions):
                        new_w = "t_" + d1.name + w[2:]
                        t1_prod = utility.multiply(d1, t1.transpose(), float(threshold_value))
                        t1_prod = t1_prod.transpose()
                        t1_prod.name = new_w

                        t2_prod = utility.multiply(d2, t2.transpose(), float(threshold_value))
                        t2_prod = t2_prod.transpose()
                        t2_prod.name = new_w

                        search_A = utility.findByValue(t_A, t1_prod.value)
                        search_B = utility.findByValue(t_B, t2_prod.value)

                        if(not (search_A and search_B and utility.compareArrays(search_A, search_B))):
                            t_A.append({'word': new_w, "vector": t1_prod})
                            t_B.append({'word': new_w, "vector": t2_prod})
                            t_w.append(new_w)
                            max_bisim_tmp = self.bisim(t1_prod, t2_prod) # matrix 
                            max_bisim = utility.min_matrix(max_bisim, max_bisim_tmp)
                            max_bisim_tmp.print_matrix()      

    def bisim(self, tau1, tau2):
        n = tau1.cols
        m = tau2.cols
        tmp_bisim = np.zeros((n, m)) 
        for i in range(0, n):
            for j in range(0, m):
                x = tau1.value[0][i]
                y = tau2.value[0][j]
                if x == y: 
                    coord = 1 
                else:
                    coord = min(x, y) / max(x, y)
                tmp_bisim[i][j] = coord 
        name = tau1.name + ' <-> ' + tau2.name
        tmp_bisim_matrix = Matrix(name, tmp_bisim)
        return tmp_bisim_matrix

