from dataclasses import asdict
import tkinter as tk
from matplotlib import projections
import numpy as np

from traceback import print_tb
from matrix import Matrix

class NerodovaKonstrukcija:
    
    n = 0 # broj stanja automata
    s = [] # vektor početnih stanja automata
    t = [] # vektor finalnih stanja automata

    s_matrices = [] # Niz koji će sadržati sve sigme
    d_matrices = [] # Niz koji će sadržati sve delte
    t_matrices = [] # Niz koji će sadržati sve tau
    s_determ_connections = [] # Kada zatvirim čvor, u ovaj niz ubacujem sa kojim čvorom treba zatvoreni čvor da povežem

    # Funkcija koja od linije koja se pročita iz fajla napraviti vektor
    def formatLineToVector(self, line):
        line = [int(num) for num in line.split(',')] # elementi u fajlu su međusobno odvojeni zarezima
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
                    matrix = np.zeros((self.n,self.n),dtype = int)
                    num = 0
                    for j in range(i, i+self.n):
                        row = self.formatLineToVector(lines[j])
                        matrix[num,:] = row
                        num += 1
                    i = j
                    matrix = Matrix("d_" + letter, matrix, False, 0, False)
                    self.d_matrices.append(matrix)

    # Funkcija koja proverava da li je stanje finalno
    def is_final(self, s):
        t = self.t_matrices[0].value
        for i in range(self.n):
            if t[i] == s[i]:
                return True
        return False

    # Determinizacija - Određivanje sigma vektora
    def determinisation(self):
        for s in self.s_matrices:
            if s.closed != True:
                for d in self.d_matrices:
                    letter = d.name[-1]
                    s_name = s.name + letter
                    s_level = len(s.name) - 1
                    s_prod = s.product_structure_matrix(d, self.n)
                    s_final = self.is_final(s_prod)

                    s_new = Matrix(s_name, s_prod, False, s_level, s_final)

                    connection = False
                    for sp in self.s_matrices:
                        if np.array_equal(sp.value, s_new.value):
                            s_new.closed = True
                            connection = sp
                            break
                    
                    if connection:
                        tuple = (s_new.name[:-1], connection.name, {'w':letter})
                    else:
                        tuple = (s_new.name[:-1], s_new.name, {'w':letter})
                            
                    self.s_matrices.append(s_new)
                    self.s_determ_connections.append(tuple)

    # Ispis početnog nedeterminističkog automata
    def print_nedeterm(self):
        print("n = ", self.n)
        self.s_matrices[0].print_matrix_in_console()
        for d in self.d_matrices:
            d.print_matrix_in_console()
        self.t_matrices[0].print_matrix_in_console()
        print("--------------------")

    # Ispis svih rezultata
    def print_results_in_console(self):
        self.print_nedeterm()
        for s in self.s_matrices:
            s.print_matrix_in_console()

    # Ispis rezultata u fajlu
    def print_results_in_file(self):
        with open('output.txt', 'w') as f:
            f.write(self.s_matrices[0].print_vector_in_file())
            for d in self.d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(self.t_matrices[0].print_vector_in_file())
            f.write("-------------------- \n")
            for s in self.s_matrices:
                f.write(s.print_vector_in_file())

    # Ispis rezultata za GUI
    def print_non_determ_results_in_GUI(self):
        str = self.s_matrices[0].print_vector_in_file()
        for d in self.d_matrices:
            str += d.print_matrix_in_file()
        str += self.t_matrices[0].print_vector_in_file()
        return str
    
    def print_determ_results_in_GUI(self):
        str = ""
        for s in self.s_matrices:
            str += s.print_vector_in_file()
        return str

    # Poziv funkcija za: učitavanje, determinizaciju i ispis rezultata
    def nerode(self, file_name):
        self.read_from_file(file_name)
        self.determinisation()
        self.print_results_in_console()
        self.print_results_in_file()