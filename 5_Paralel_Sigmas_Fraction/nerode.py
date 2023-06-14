from dataclasses import asdict
import tkinter as tk
from matplotlib import projections
import numpy as np
from traceback import print_tb
from matrix import Matrix
from fractions import Fraction

class NerodovaKonstrukcija:
    
    n = 0 # broj stanja automata
    s = [] # vektor početnih stanja automata
    t = [] # vektor finalnih stanja automata

    # Nizovi koji služe za računanje sigma vektora, bez ograničenja
    s_matrices = [] # Niz koji će sadržati sve sigme
    d_matrices = [] # Niz koji će sadržati sve delte
    t_matrices = [] # Niz koji će sadržati sve tau

    # Nizovi koji služe za računanje sigma vektora, sa ograničenjem E
    s_matrices_e = [] # Niz koji će sadržati sve sigme
    d_matrices_e = [] # Niz koji će sadržati sve delte
    t_matrices_e = [] # Niz koji će sadržati sve tau

    # Funkcija koja od linije koja se pročita iz fajla napravi vektor
    def formatLineToVector(self, line):
        line = [Fraction(num) for num in line.split(',')] # elementi u fajlu su međusobno odvojeni zarezima
        vector = np.array(line)
        return vector
    
    # Funkcija za čitanje iz fajla
    def read_from_file(self, file_name):
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
                    self.n = int(line)

                # Ako pročita reč "start", to znači da se u narednom redu (i += 1) nalazi vektor inicijalnih stanja automata
                elif "start" in line:
                    i += 1
                    self.s = self.formatLineToVector(lines[i]) # od pročitane linije napravimo vektor
                    matrix = Matrix("s_", self.s, False, 0, False) # pošto je ovo vektor/matrica početnih stanja, kreiramo objekat klase Matrix
                    self.s_matrices.append(matrix) # dodamo inicijalnu matricu u skup svih sigma matrica
                    self.s_matrices_e.append(matrix) # dodamo inicijalnu matricu u skup svih sigma matrica

                # Ako pročita reč "end", to znači da se u narednom redu (i += 1) nalazi vektor finalnih stanja automata
                elif "end" in line:
                    i += 1  
                    self.t = self.formatLineToVector(lines[i]) # od pročitane linije napravimo vektor
                    matrix = Matrix("t_", self.t, False, 0, True) # pošto je ovo vektor/matrica početnih stanja, kreiramo objekat klase Matrix
                    self.t_matrices.append(matrix)
               
                # Ako pročita reč transition, to znači da se u narednim redovima nalaze matrice prelaza za dati automat
                elif "transition" in line:
                    letter = line[-2]
                    i += 1  
                    matrix = np.zeros((self.n,self.n),dtype = Fraction)
                    num = 0
                    for j in range(i, i+self.n):
                        row = self.formatLineToVector(lines[j])
                        matrix[num,:] = row
                        num += 1
                    i = j
                    matrix = Matrix("d_" + letter, matrix, False, 0, False)
                    self.d_matrices.append(matrix)

    # Determinizacija - Određivanje sigma vektora
    def determinisation(self):
        i = 0 # Indeks matrice u nizu
        for s in self.s_matrices_e:
            if s.closed != True:
                for d in self.d_matrices:
                    letter = d.name[-1]
                    s_name = s.name + letter
                    s_level = len(s.name) - 1
                    s_final = False

                    # Računamo matrice sa ograničenjem
                    s_prod_e = s.product_structure_matrix_bounded(d, self.n)
                    s_closed = False
                    for sp in self.s_matrices_e:
                        if np.array_equal(sp.value, s_prod_e):
                            s_closed = True
                            break
                    s_new = Matrix(s_name, s_prod_e, s_closed, s_level, s_final)
                    self.s_matrices_e.append(s_new)

                    # Računamo za istu reč matrice bez ograničenja
                    s1 = self.s_matrices[i]
                    s_prod = s1.product_structure_matrix(d, self.n)
                    s_closed = False
                    for sp in self.s_matrices:
                        if np.array_equal(sp.value, s_prod):
                            s_closed = True
                            break
                    s_new = Matrix(s_name, s_prod, s_closed, s_level, s_final)
                    self.s_matrices.append(s_new)
            i = i + 1

    # Ispis u fajlu
    def print_results_in_file(self, file, sigmas):
        with open(file, 'w') as f:
            f.write(self.s_matrices[0].print_vector_in_file())
            for d in self.d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(self.t_matrices[0].print_vector_in_file())
            f.write("-------------------- \n")
            for s in sigmas:
                f.write(s.print_vector_in_file())

    # Ispis u GUI
    def print_initial_in_GUI(self):
        str = self.s_matrices[0].print_vector_in_file()
        for d in self.d_matrices:
            str += d.print_matrix_in_file()
        str += self.t_matrices[0].print_vector_in_file()
        return str
    
    def print_results_in_GUI(self):
        str = ""
        for s in self.s_matrices:
            str += s.print_vector_in_file()
        return str

    def print_bounded_results_in_GUI(self):
        str = ""
        for s in self.s_matrices_e:
            str += s.print_vector_in_file()
        return str

    # Poziv funkcija za: učitavanje, determinizaciju i ispis rezultata
    def nerode(self, file_name):
        self.read_from_file(file_name)
        self.determinisation()
        self.print_results_in_file('output_without_bound.txt', self.s_matrices)
        self.print_results_in_file('output_with_bound.txt', self.s_matrices_e)