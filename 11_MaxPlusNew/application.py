from threading import local
from time import time
import tkinter as tk
from cmath import inf
from tkinter import filedialog
from tkinter import messagebox
from automaton import Automaton
from matrix import Matrix
import utility

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")

        # Initialize variables
        self.selected_file_1 = ""
        self.selected_file_2 = ""
        
        # Create GUI elements
        self.button_browse_1 = tk.Button(self.root, text="Browse File 1", command=self.browse_file_1)
        self.button_browse_1.grid(row=0, column=0, padx=10, pady=5)
        self.selected_file_label_1 = tk.Label(self.root, text="Selected File 1: ")
        self.selected_file_label_1.grid(row=0, column=1, padx=10, pady=5)

        self.button_browse_2 = tk.Button(self.root, text="Browse File 2", command=self.browse_file_2)
        self.button_browse_2.grid(row=1, column=0, padx=10, pady=5)
        self.selected_file_label_2 = tk.Label(self.root, text="Selected File 2: ")
        self.selected_file_label_2.grid(row=1, column=1, padx=10, pady=5)

        self.checkbox_values = {
            "Forward Simulation": tk.BooleanVar(),
            "Backward Simulation": tk.BooleanVar(),
            "Forward Bisimulation": tk.BooleanVar(),
            "Backward Bisimulation": tk.BooleanVar(),
            "Forward-Backward Bisimulation": tk.BooleanVar(),
            "Backward-Forward Bisimulation": tk.BooleanVar()
        }

        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        for i, (checkbox_text, checkbox_var) in enumerate(self.checkbox_values.items()):
            checkbox = tk.Checkbutton(self.checkbox_frame, text=checkbox_text, variable=checkbox_var)
            checkbox.grid(row=i, column=0, sticky='w')

        self.button_compute = tk.Button(self.root, text="Compute", command=self.compute)
        self.button_compute.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def browse_file_1(self):
        self.selected_file_1 = filedialog.askopenfilename()
        if self.selected_file_1:
            self.selected_file_label_1.config(text="Selected File 1: " + self.selected_file_1)

    def browse_file_2(self):
        self.selected_file_2 = filedialog.askopenfilename()
        if self.selected_file_2:
            self.selected_file_label_2.config(text="Selected File 2: " + self.selected_file_2)

    def compute(self):
        if not self.selected_file_1:
            messagebox.showinfo("Error", "Please choose File 1.")
        elif not self.selected_file_2:
            messagebox.showinfo("Error", "Please choose File 2.")
        else:
            selected_checkboxes = []
            for checkbox_text, checkbox_var in self.checkbox_values.items():
                if checkbox_var.get():
                    selected_checkboxes.append(checkbox_text)

            if len(selected_checkboxes) == 0:
                messagebox.showinfo("Error", "Please select at least one checkbox.")
            else:
                automaton1 = Automaton(self.selected_file_1)
                automaton2 = Automaton(self.selected_file_2)

                if len(automaton1.transitions) != len(automaton2.transitions):
                    print("Number of transitions in Automaton 1 and Automaton 2 must be the same.")
                    return

                # Perform different actions based on selected checkboxes
                for checkbox_text in selected_checkboxes:

                    if checkbox_text == "Forward Simulation":
                        # tau_A \ tau_B
                        U_1_fs = utility.right_residual(automaton1.tau, automaton2.tau)

                        n = 0
                        while True:
                            local_min = Matrix("local_min", [[inf] * U_1_fs.cols for _ in range(U_1_fs.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]
                                
                                U_1_fs_T = U_1_fs.transpose()
                                left = utility.left_residual(M_x_A, utility.multiply(M_x_B, U_1_fs_T))
                                local_min = utility.matrix_min(local_min, left)
                            U_2_fs = utility.matrix_min(local_min, U_1_fs)

                            n+=1
                            if U_1_fs.value == U_2_fs.value or n == 10:
                                break
                            else:
                                U_1_fs = U_2_fs
                                U_1_fs.print_matrix()

                    if checkbox_text == "Backward Simulation":
                        # sigma_A \ sigma_B
                        U_1_bs = utility.right_residual(automaton1.sigma, automaton2.sigma)

                        M_x_A = automaton1.transitions[0]
                        M_x_B = automaton2.transitions[0]
                        
                        times = utility.multiply(U_1_bs, M_x_B)
                        right = utility.right_residual(M_x_A, times)
                        right.print_matrix()

                    if checkbox_text == "Forward Bisimulation":
                        # Do something for Forward Bisimulation
                        print("Performing Forward Bisimulation...")
                    if checkbox_text == "Backward Bisimulation":
                        # Do something for Backward Bisimulation
                        print("Performing Backward Bisimulation...")
                    if checkbox_text == "Forward-Backward Bisimulation":
                        # Do something for Forward-Backward Bisimulation
                        print("Performing Forward-Backward Bisimulation...")
                    if checkbox_text == "Backward-Forward Bisimulation":
                        # Do something for Backward-Forward Bisimulation
                        print("Performing Backward-Forward Bisimulation...")

                


                
             