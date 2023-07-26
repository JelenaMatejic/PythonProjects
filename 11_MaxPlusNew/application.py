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
                    tau_A = automaton1.tau # row vector
                    tau_B = automaton2.tau # row vector
                    tau_A_T = tau_A.transpose() # column vector
                    tau_B_T = tau_B.transpose() # column vector
                    sigma_A = automaton1.sigma # row vector
                    sigma_B = automaton2.sigma # row vector
                    sigma_A_T = sigma_A.transpose() # column vector
                    sigma_B_T = sigma_B.transpose() # column vector

                    if checkbox_text == "Forward Simulation":
                        print("----- Forward Simulation -----")
                        # U_1_fs = tau_A \ tau_B
                        U_1_fs = utility.right_residual(tau_A, tau_B)
                        U_1_fs.name = "U_1_fs"
                        U_1_fs.print_matrix()

                        n = 1
                        while True:
                            n+=1
                            name = "U_" + str(n) + "_fs"
                            local_min = Matrix(name, [[inf] * U_1_fs.cols for _ in range(U_1_fs.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]
                                
                                U_1_fs_T = U_1_fs.transpose()
                                left = utility.left_residual(utility.multiply(M_x_B, U_1_fs_T), M_x_A)
                                left_T = left.transpose()
                                local_min = utility.matrix_min(local_min, left_T)
                            U_2_fs = utility.matrix_min(local_min, U_1_fs)

                            if U_1_fs.value == U_2_fs.value or n == 10:
                                break
                            else:
                                U_2_fs.name = name
                                U_1_fs = U_2_fs
                                U_1_fs.print_matrix()
                                

                    if checkbox_text == "Backward Simulation":
                        print("----- Backward Simulation -----")
                        # sigma_A \ sigma_B
                        U_1_bs = utility.right_residual(sigma_A, sigma_B)
                        U_1_bs.name = "U_1_bs"
                        U_1_bs.print_matrix()

                        n = 1
                        while True:
                            n+=1
                            name = "U_" + str(n) + "_bs"
                            local_min = Matrix(name, [[inf] * U_1_bs.cols for _ in range(U_1_bs.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]
                                
                                right = utility.right_residual(M_x_A, utility.multiply(U_1_bs, M_x_B))
                                local_min = utility.matrix_min(local_min, right)
                            U_2_bs = utility.matrix_min(local_min, U_1_bs)

                            if U_1_bs.value == U_2_bs.value or n == 10:
                                break
                            else:
                                U_2_bs.name = name
                                U_1_bs = U_2_bs
                                U_1_bs.print_matrix()

                    if checkbox_text == "Forward Bisimulation":
                        print("----- Forward Bisimulation -----")
                        # (tau_A \ tau_B) i (tau_A / tau_B)
                        U_1_fb = utility.matrix_min(utility.right_residual(tau_A, tau_B), utility.left_residual(tau_A_T, tau_B_T))
                        U_1_fb.name = "U_1_fb"
                        U_1_fb.print_matrix()

                        n = 1
                        while True:
                            n+=1
                            name = "U_" + str(n) + "_fb"
                            local_min = Matrix(name, [[inf] * U_1_fb.cols for _ in range(U_1_fb.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]
                                U_1_fb_T = U_1_fb.transpose()

                                left1 = utility.left_residual(utility.multiply(M_x_B, U_1_fb_T), M_x_A)
                                left1_T = left1.transpose()

                                left2 = utility.left_residual(utility.multiply(M_x_A, U_1_fb), M_x_B)

                                left_min = utility.matrix_min(left1_T, left2)
                                local_min = utility.matrix_min(local_min, left_min)
                            U_2_fb = utility.matrix_min(local_min, U_1_fb)

                            if U_1_fb.value == U_2_fb.value or n == 10:
                                break
                            else:
                                U_2_fb.name = name
                                U_1_fb = U_2_fb
                                U_1_fb.print_matrix()

                    if checkbox_text == "Backward Bisimulation":
                        print("----- Backward Bisimulation -----")
                        # (sigma_A \ sigma_B) i (sigma_A / sigma_B)
                        U_1_bb = utility.matrix_min(utility.right_residual(sigma_A, sigma_B), utility.left_residual(sigma_A_T, sigma_B_T))
                        U_1_bb.name = "U_1_bb"
                        U_1_bb.print_matrix()

                        n = 1
                        while True:
                            n+=1
                            name = "U_" + str(n) + "_bb"
                            local_min = Matrix(name, [[inf] * U_1_bb.cols for _ in range(U_1_bb.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]
                                U_1_bb_T = U_1_bb.transpose()

                                right1 = utility.right_residual(M_x_A, utility.multiply(U_1_bb, M_x_B))
                                right2 = utility.right_residual(M_x_B, utility.multiply(U_1_bb_T, M_x_A))
                                right2_T = right2.transpose()

                                right_min = utility.matrix_min(right1, right2_T)
                                local_min = utility.matrix_min(local_min, right_min)
                            U_2_bb = utility.matrix_min(local_min, U_1_bb)

                            if U_1_bb.value == U_2_bb.value or n == 10:
                                break
                            else:
                                U_2_bb.name = name
                                U_1_bb = U_2_bb
                                U_1_bb.print_matrix()

                    if checkbox_text == "Forward-Backward Bisimulation":
                        print("----- Forward-Backward Bisimulation -----")
                        # (sigma_A / sigma_B) i (tau_A \ tau_B)
                        U_1_fbb = utility.matrix_min(utility.left_residual(sigma_A_T, sigma_B_T), utility.right_residual(tau_A, tau_B))
                        U_1_fbb.name = "U_1_fbb"
                        U_1_fbb.print_matrix()

                        n = 1
                        while True:
                            n+=1
                            name = "U_" + str(n) + "_fbb"
                            local_min = Matrix(name, [[inf] * U_1_fbb.cols for _ in range(U_1_fbb.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]
                                U_1_fbb_T = U_1_fbb.transpose()

                                left = utility.left_residual(utility.multiply(M_x_B, U_1_fbb_T), M_x_A)
                                left_T = left.transpose()

                                right = utility.right_residual(M_x_B, utility.multiply(U_1_fbb_T, M_x_A))
                                right_T = right.transpose()

                                left_right_min = utility.matrix_min(left_T, right_T)
                                local_min = utility.matrix_min(local_min, left_right_min)
                            U_2_fbb = utility.matrix_min(local_min, U_1_fbb)

                            if U_1_fbb.value == U_2_fbb.value or n == 10:
                                break
                            else:
                                U_2_fbb.name = name
                                U_1_fbb = U_2_fbb
                                U_1_fbb.print_matrix()

                    if checkbox_text == "Backward-Forward Bisimulation":
                        print("----- Backward-Forward Bisimulation -----")
                        # (sigma_A \ sigma_B) i (tau_A / tau_B)
                        U_1_bfb = utility.matrix_min(utility.right_residual(sigma_A, sigma_B), utility.left_residual(tau_A_T, tau_B_T))
                        U_1_bfb.name = "U_1_bfb"
                        U_1_bfb.print_matrix()

                        n = 1
                        while True:
                            n+=1
                            name = "U_" + str(n) + "_bfb"
                            local_min = Matrix(name, [[inf] * U_1_bfb.cols for _ in range(U_1_bfb.rows)])
                            for i in range(len(automaton1.transitions)):
                                M_x_A = automaton1.transitions[i]
                                M_x_B = automaton2.transitions[i]

                                right = utility.right_residual(M_x_A, utility.multiply(U_1_bfb, M_x_B))
                                left = utility.left_residual(utility.multiply(M_x_A, U_1_bfb), M_x_B)

                                right_left_min = utility.matrix_min(right, left)
                                local_min = utility.matrix_min(local_min, right_left_min)
                            U_2_bfb = utility.matrix_min(local_min, U_1_bfb)

                            if U_1_bfb.value == U_2_bfb.value or n == 10:
                                break
                            else:
                                U_2_bfb.name = name
                                U_1_bfb = U_2_bfb
                                U_1_bfb.print_matrix()


                


                
             