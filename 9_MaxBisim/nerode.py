from dataclasses import asdict
from hashlib import new
import tkinter as tk
from matplotlib import projections
import numpy as np
from traceback import print_tb
from matrix import Matrix
from fractions import Fraction

class NerodovaKonstrukcija:
    
    def __init__(self) -> None:
        self.n = 0 # broj stanja automata
        self.s = [] # vektor početnih stanja automata
        self.t = [] # vektor finalnih stanja automata

        # Nizovi koji služe za računanje sigma vektora, bez ograničenja
        self.s_matrices = [] # Niz koji će sadržati sve sigme
        self.d_matrices = [] # Niz koji će sadržati sve delte
        self.t_matrices = [] # Niz koji će sadržati sve tau

        # Nizovi koji služe za računanje sigma vektora, sa ograničenjem E
        self.s_matrices_e = [] # Niz koji će sadržati sve sigme
        self.d_matrices_e = [] # Niz koji će sadržati sve delte
        self.t_matrices_e = [] # Niz koji će sadržati sve tau

        # Niz koji će sadržati sve matrice za bisimulacije
        self.t_matrices_bisim = []

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
                    self.t_matrices_e.append(matrix)
               
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
    def determinisation_sigmas(self, level, e, fraction):
        i = 0 # Indeks matrice u nizu
        for s in self.s_matrices_e:
            if s.level == level:
                break
            if s.closed != True:
                for d in self.d_matrices:
                    letter = d.name[-1]
                    s_name = s.name + letter
                    s_level = len(s.name) - 1

                    # Računamo matrice sa ograničenjem
                    s_prod_e = s.product_structure_sigmas(d, self.n, e, fraction)
                    s_closed = False
                    for sp in self.s_matrices_e:
                        if np.array_equal(sp.value, s_prod_e):
                            s_closed = True
                            break
                    s_new = Matrix(s_name, s_prod_e, s_closed, s_level, False)
                    self.s_matrices_e.append(s_new)

                    # Računamo za istu reč matrice bez ograničenja i zato za e prosleđujemo 0
                    s1 = self.s_matrices[i]
                    s_prod = s1.product_structure_sigmas(d, self.n, 0, fraction)
                    s_closed = False
                    for sp in self.s_matrices:
                        if np.array_equal(sp.value, s_prod):
                            s_closed = True
                            break
                    s_new = Matrix(s_name, s_prod, s_closed, s_level, False)
                    self.s_matrices.append(s_new)
            i = i + 1

    # Determinizacija - Određivanje tau vektora
    def determinisation_taus(self, level, e, fraction):
        i = 0 # Indeks matrice u nizu
        for t in self.t_matrices_e:
            if t.level == level:
                break
            if t.closed != True:
                for d in self.d_matrices:
                    letter = d.name[-1]
                    t_name = t.name + letter
                    t_level = len(t.name) - 1

                    # Računamo matrice sa ograničenjem
                    t_prod_e = d.product_structure_taus(t, self.n, e, fraction)
                    t_closed = False
                    for tp in self.t_matrices_e:
                        if np.array_equal(tp.value, t_prod_e):
                            t_closed = True
                            break
                    t_new = Matrix(t_name, t_prod_e, t_closed, t_level, False)
                    self.t_matrices_e.append(t_new)

                    # Računamo za istu reč matrice bez ograničenja
                    t1 = self.t_matrices[i]
                    t_prod = d.product_structure_taus(t1, self.n, 0, fraction)
                    t_closed = False
                    for tp in self.t_matrices:
                        if np.array_equal(tp.value, t_prod):
                            t_closed = True
                            break
                    t_new = Matrix(t_name, t_prod, t_closed, t_level, False)
                    self.t_matrices.append(t_new)
            i = i + 1
        
    # Računanje svih bisimulacija i najmanje bisimulacije
    def bisim(self):
        max_bisim =  np.ones((self.n, self.n),dtype = Fraction)
        
        for t in self.t_matrices_e:
            if t.closed == False:
                C = np.ones((self.n, self.n),dtype = Fraction)
                for i in range(0, self.n):
                    for j in range(0, self.n):
                        if t.value[i] == t.value[j]:
                            coord = 1
                        else:
                            coord = min(t.value[i], t.value[j]) / max(t.value[i], t.value[j])
                        C[i][j] = coord
                        max_bisim[i][j] = min(max_bisim[i][j], coord)
                name = t.name + ' <-> ' + t.name
                matrix_c = Matrix(name, C, False, 0, False)
                self.t_matrices_bisim.append(matrix_c)
        matrix_max_bisim = Matrix('Maks.Bisim.', max_bisim, False, 0, False)
        self.t_matrices_bisim.append(matrix_max_bisim)
        return matrix_max_bisim

    # Ispis u fajlu
    def print_results_in_file(self, file, vectors):
        with open(file, 'w') as f:
            f.write(self.s_matrices[0].print_vector_in_file())
            for d in self.d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(self.t_matrices[0].print_vector_in_file())
            f.write("-------------------- \n")
            for v in vectors:
                f.write(v.print_vector_in_file())

    def print_bisim_results_in_file(self, file):
        with open(file, 'w') as f:
            f.write(self.s_matrices[0].print_vector_in_file())
            for d in self.d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(self.t_matrices[0].print_vector_in_file())
            f.write("-------------------- \n")
            for t in self.t_matrices_bisim:
                f.write(t.print_matrix_in_file())

    # Ispis u GUI
    def print_initial_in_GUI(self):
        str = self.s_matrices[0].print_vector_in_file()
        for d in self.d_matrices:
            str += d.print_matrix_in_file()
        str += self.t_matrices[0].print_vector_in_file()
        return str
    
    def print_results_in_GUI(self, vectors):
        str = ""
        for v in vectors:
            str += v.print_vector_in_file()
        return str

    def print_bisim_in_GUI(self):
        str = ""
        for t in self.t_matrices_bisim:
            str += t.print_matrix_in_file()
            t.print_matrix_in_console()
        return str

    # Poziv funkcija za: učitavanje, determinizaciju i ispis rezultata
    def nerode(self, file_name, determinisation_type, level, threshold):
        self.read_from_file(file_name)
        if determinisation_type == "Word length":
            self.determinisation_sigmas(level, threshold, False)
            self.determinisation_taus(level, threshold, False)
            self.print_results_in_file('output1.txt', self.s_matrices)
            self.print_results_in_file('output2.txt', self.t_matrices)
            return [self.print_results_in_GUI(self.s_matrices), self.print_results_in_GUI(self.t_matrices)]
        elif determinisation_type == "Threshold":
            self.determinisation_sigmas(level, threshold, False)
            self.determinisation_taus(level, threshold, False)
            self.print_results_in_file('output1.txt', self.s_matrices_e)
            self.print_results_in_file('output2.txt', self.t_matrices_e)
            return [self.print_results_in_GUI(self.s_matrices_e), self.print_results_in_GUI(self.t_matrices_e)]
        elif determinisation_type == "Threshold sigmas (decimal)":
            self.determinisation_sigmas(level, threshold, False)
            self.print_results_in_file('output1.txt', self.s_matrices)
            self.print_results_in_file('output2.txt', self.s_matrices_e)
            return [self.print_results_in_GUI(self.s_matrices), self.print_results_in_GUI(self.s_matrices_e)]
        elif determinisation_type == "Threshold taus (decimal)":
            self.determinisation_taus(level, threshold, False)
            self.print_results_in_file('output1.txt', self.t_matrices)
            self.print_results_in_file('output2.txt', self.t_matrices_e)
            return [self.print_results_in_GUI(self.t_matrices), self.print_results_in_GUI(self.t_matrices_e)]
        elif determinisation_type == "Threshold sigmas (fraction)":
            self.determinisation_sigmas(level, threshold, True)
            self.print_results_in_file('output1.txt', self.s_matrices)
            self.print_results_in_file('output2.txt', self.s_matrices_e)
            return [self.print_results_in_GUI(self.s_matrices), self.print_results_in_GUI(self.s_matrices_e)]
        elif determinisation_type == "Threshold taus (fraction)":
            self.determinisation_taus(level, threshold, True)
            self.print_results_in_file('output1.txt', self.t_matrices)
            self.print_results_in_file('output2.txt', self.t_matrices_e)
            return [self.print_results_in_GUI(self.t_matrices), self.print_results_in_GUI(self.t_matrices_e)]
        else:
            self.determinisation_taus(level, threshold, True)
            max_bisim_matrix = self.bisim()
            self.print_results_in_file('output1.txt', self.t_matrices_e)
            self.print_bisim_results_in_file('output2.txt')
            return [self.print_results_in_GUI(self.t_matrices_e), max_bisim_matrix.print_matrix_in_file()[12:]] # Krećemo od 12 da ne bi ispisivao naaziv matrice Max.Bisim.\n