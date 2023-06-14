from dataclasses import asdict
from hashlib import new
import tkinter as tk
from turtle import right
from unicodedata import decimal
from matplotlib import projections
import numpy as np
from traceback import print_tb
from matrix import Matrix
from fractions import Fraction

class NerodovaKonstrukcija:
    
    def __init__(self) -> None:
        self.n = 0 # broj stanja A automata
        self.s_matrices = [] # Niz koji će sadržati sve sigme automata A
        self.d_matrices = [] # Niz koji će sadržati sve delte automata A
        self.t_matrices = [] # Niz koji će sadržati sve tau automata A
        self.t_matrices_bisim = []  # Niz svih bisimulacija nad automatom A

        self.n_2 = 0 # broj stanja B automata
        self.s_matrices_2 = [] # Niz koji će sadržati sve sigme automata B
        self.d_matrices_2 = [] # Niz koji će sadržati sve delte automata B
        self.t_matrices_2 = [] # Niz koji će sadržati sve tau automata B
        self.t_matrices_bisim_2 = []  # Niz svih bisimulacija nad automatom B

    # Funkcija koja od linije koja se pročita iz fajla napravi vektor
    def formatLineToVector(self, line):
        line = [Fraction(num) for num in line.split(',')] # elementi u fajlu su međusobno odvojeni zarezima
        vector = np.array(line)
        return vector
    
    # Funkcija za čitanje iz fajla
    def read_from_file(self, file_name, states, s_matrices, d_matrices, t_matrices):
        file = open(file_name, "r")
        with file:
            # Pročitaćemo ceo fajl, a onda se kretati liniju po liniju u njemu
            lines = file.readlines() 
            for i in range(0, len(lines)):
                line = lines[i]
                # Ako pročita reč "states", to znači da se u narednom redu (i += 1) nalazi broj stanja automata
                if "states" in line:
                    i += 1
                    line = lines[i]
                    states = int(line)

                # Ako pročita reč "start", to znači da se u narednom redu (i += 1) nalazi vektor inicijalnih stanja automata
                elif "start" in line:
                    i += 1
                    s = [self.formatLineToVector(lines[i])] # od pročitane linije napravimo vektor, ali stavljamo ga u [ ] da postane matrica
                    matrix = Matrix("s_", s, False, 0, False) # pošto je ovo vektor/matrica početnih stanja, kreiramo objekat klase Matrix
                    s_matrices.append(matrix) # dodamo inicijalnu matricu u skup svih sigma matrica

                # Ako pročita reč "end", to znači da se u narednom redu (i += 1) nalazi vektor finalnih stanja automata
                elif "end" in line:
                    i += 1  
                    t = [self.formatLineToVector(lines[i])] # od pročitane linije napravimo vektor, ali stavljamo ga u [ ] da postane matrica
                    t = np.transpose(t)
                    matrix = Matrix("t_", t, False, 0, True) # pošto je ovo vektor/matrica početnih stanja, kreiramo objekat klase Matrix
                    t_matrices.append(matrix)
               
                # Ako pročita reč transition, to znači da se u narednim redovima nalaze matrice prelaza za dati automat
                elif "transition" in line:
                    letter = line[-2]
                    i += 1  
                    matrix = np.zeros((states,states),dtype = Fraction)
                    num = 0
                    for j in range(i, i+states):
                        row = self.formatLineToVector(lines[j])
                        matrix[num,:] = row
                        num += 1
                    i = j
                    matrix = Matrix("d_" + letter, matrix, False, 0, False)
                    d_matrices.append(matrix)

    def determinisation(self, level, e, fraction, arr_vectors, vector_left):
        for v in arr_vectors:
            if v.level == level:
                break
            if v.closed != True:
                for d in self.d_matrices:
                    letter = d.name[-1]
                    new_name = v.name + letter
                    new_level = len(v.name) - 1

                    # Računamo matrice sa ograničenjem
                    if vector_left:
                        product = v.multiply_matrices(d, e, fraction)
                    else:
                        product = d.multiply_matrices(v, e, fraction)

                    closed = False
                    for vp in arr_vectors:
                        if np.array_equal(vp.value, product):
                            closed = True
                            break
                    new_matrix = Matrix(new_name, product, closed, new_level, False)
                    arr_vectors.append(new_matrix)

    def determinisation2(self, level, e, fraction, arr_vectors, d_matrices, vector_left):
        for v in arr_vectors:
            if v.level == level:
                break
            for d in d_matrices:
                letter = d.name[-1]
                new_name = v.name + letter
                new_level = len(v.name) - 1

                # Računamo matrice sa ograničenjem
                if vector_left:
                    product = v.multiply_matrices(d, e, fraction)
                else:
                    product = d.multiply_matrices(v, e, fraction)

                closed = False
                for vp in arr_vectors:
                    if np.array_equal(vp.value, product):
                        closed = True
                        break
                new_matrix = Matrix(new_name, product, closed, new_level, False)
                arr_vectors.append(new_matrix)
        
    # Računanje svih bisimulacija i najmanje bisimulacije
    def bisim(self, n, t_matrices, t_matrices_bisim):
        max_bisim =  np.ones((n, n),dtype = Fraction) # Matrica maksimalne bisimulacije
        for t in t_matrices:
            if t.closed == False:
                C = np.ones((n, n),dtype = Fraction) # Matrica trenutne bisimulacije
                for i in range(0, n):
                    for j in range(0, n):
                        if t.value[i][0] == t.value[j][0]: 
                            coord = 1   # Ako su vrednosti iste, onda je coord = 1
                        else:
                            coord = min(t.value[i][0], t.value[j][0]) / max(t.value[i][0], t.value[j][0]) # Računamo coord
                        C[i][j] = coord # Upisujemo kao coord trenutne simulacije
                        max_bisim[i][j] = min(max_bisim[i][j], coord) # Tražimo koordinatu koja je minimalna do sada
                name = t.name + ' <-> ' + t.name
                matrix_c = Matrix(name, C, False, 0, False) # Kreiramo matricu tekuće simulacije
                t_matrices_bisim.append(matrix_c) # Dodamo tu matricu u niz svih matrica
        matrix_max_bisim = Matrix('Maks.Bisim.', max_bisim, False, 0, False) # Kreiramo objekat najveće bisimulacije
        t_matrices_bisim.append(matrix_max_bisim) # Na kraj svih bisimulacija, dodamo najveću
        return matrix_max_bisim

    def product_equivalence(self, vector1, vector2):
        C = np.zeros((len(vector1), len(vector2)),dtype = Fraction)
        for i in range(len(vector1)):
            for j in range(len(vector2)):
                a = vector1[i][0] # koord. reda iz prve matrice
                b = vector2[j][0] # koord. reda iz druge matrice
                if a == b: 
                    coord = 1   # Ako su vrednosti iste, onda je coord = 1
                else:
                    coord =  min(a, b) / max(a, b)
                C[i][j] = coord
        return C
    
    def paralel_bisim(self, t_matrices_A, t_matrices_B):
        vector1 = t_matrices_A[0].value
        vector2 = t_matrices_B[0].value
        n = len(vector1)
        m = len(vector2)
        max_bisim = np.ones((n, m),dtype = Fraction)
        for ind in range(len(t_matrices_A)):
            vector1 = t_matrices_A[ind].value
            vector2 = t_matrices_B[ind].value
            C = np.ones((n, m),dtype = Fraction)
            for i in range(n):
                for j in range(m):
                    a = vector1[i][0] # koord. reda iz prve matrice
                    b = vector2[j][0] # koord. reda iz druge matrice
                    if a == b: 
                        coord = 1   # Ako su vrednosti iste, onda je coord = 1
                    else:
                        coord =  min(a, b) / max(a, b)
                    C[i][j] = coord
                    max_bisim[i][j] = min(coord, max_bisim[i][j]) 
            name = t_matrices_A[ind].name + "<->" + t_matrices_B[ind].name
            matrix_C = Matrix(name, C, False, 0, False)
            self.t_matrices_bisim_2.append(matrix_C) 

        matrix_max_bisim = Matrix('Maks.Bisim.', max_bisim, False, 0, False) # Kreiramo objekat najveće bisimulacije
        return matrix_max_bisim

    # Ispis u fajlu
    def print_results_in_file(self, file, vectors):
        with open(file, 'w') as f:
            f.write(self.s_matrices[0].print_matrix_in_file())
            for d in self.d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(self.t_matrices[0].print_matrix_in_file())
            f.write("-------------------- \n")
            for v in vectors:
                f.write(v.print_matrix_in_file())

    def print_bisim_results_in_file(self, file, s_matrices, d_matrices, t_matrices, t_matrices_bisim):
        with open(file, 'w') as f:
            f.write(s_matrices[0].print_matrix_in_file())
            for d in d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(t_matrices[0].print_matrix_in_file())
            f.write("-------------------- \n")
            for t in t_matrices_bisim:
                f.write(t.print_matrix_in_file())

    # Ispis u GUI
    def print_initial_in_GUI(self):
        str = self.s_matrices[0].print_matrix_in_file()
        for d in self.d_matrices:
            str += d.print_matrix_in_file()
        str += self.t_matrices[0].print_matrix_in_file()
        return str
    
    def print_results_in_GUI(self, vectors):
        str = ""
        for v in vectors:
            str += v.print_matrix_in_file()
        return str

    # Poziv funkcija za: učitavanje, determinizaciju i ispis rezultata
    def nerode(self, file_name, file_name_2, determinisation_type, level, threshold):
        self.read_from_file(file_name, self.n, self.s_matrices, self.d_matrices, self.t_matrices)
        self.n = len(self.t_matrices[0].value)

        if determinisation_type == "Bisimulation":
            self.determinisation(level, threshold, Fraction, self.t_matrices, False)
            max_bisim_matrix = self.bisim(self.n, self.t_matrices, self.t_matrices_bisim)
            self.print_results_in_file('output1.txt', self.t_matrices)
            self.print_bisim_results_in_file('output2.txt', self.s_matrices, self.d_matrices, self.t_matrices, self.t_matrices_bisim)
            return [self.print_results_in_GUI(self.t_matrices), max_bisim_matrix.print_matrix_in_file()[12:]] # Krećemo od 12 da ne bi ispisivao naaziv matrice Max.Bisim.\n
        elif determinisation_type == "Bisimulation 2":
            self.read_from_file(file_name_2, self.n_2, self.s_matrices_2, self.d_matrices_2, self.t_matrices_2)
            self.n_2 = len(self.t_matrices_2[0].value)
            # 
            self.determinisation(level, threshold, Fraction, self.t_matrices, False)
            self.determinisation(level, threshold, Fraction, self.t_matrices_2, False)
            #
            if self.t_matrices[-1].level > self.t_matrices_2[-1].level:
                max_level = self.t_matrices[-1].level
            else:
                max_level = self.t_matrices_2[-1].level
            #
            self.t_matrices = [self.t_matrices[0]]
            self.t_matrices_2 = [self.t_matrices_2[0]]
            #
            self.determinisation2(max_level, threshold, Fraction, self.t_matrices, self.d_matrices, False)
            self.determinisation2(max_level, threshold, Fraction, self.t_matrices_2, self.d_matrices_2, False)
            #
            max_bisim_matrix = self.paralel_bisim(self.t_matrices, self.t_matrices_2)
            self.print_results_in_file('output1.txt', self.t_matrices_bisim_2)
            return [self.print_results_in_GUI(self.t_matrices_bisim_2), max_bisim_matrix.print_matrix_in_file()[12:]] # Krećemo od 12 da ne bi ispisivao naaziv matrice Max.Bisim.\n
        elif determinisation_type == "Threshold (decimal)":
            self.determinisation(level, threshold, float, self.s_matrices, True)
            self.determinisation(level, threshold, float, self.t_matrices, False)
            self.print_results_in_file('output1.txt', self.s_matrices)
            self.print_results_in_file('output2.txt', self.t_matrices)
            return [self.print_results_in_GUI(self.s_matrices), self.print_results_in_GUI(self.t_matrices)]
        else:
            self.determinisation(level, threshold, Fraction, self.s_matrices, True)
            self.determinisation(level, threshold, Fraction, self.t_matrices, False)
            self.print_results_in_file('output1.txt', self.s_matrices)
            self.print_results_in_file('output2.txt', self.t_matrices)
            return [self.print_results_in_GUI(self.s_matrices), self.print_results_in_GUI(self.t_matrices)]