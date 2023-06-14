from dataclasses import asdict
from hashlib import new
import tkinter as tk
from tokenize import String
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
        self.s_matrices = [] # Niz koji će sadržati sve sigme - početne vektore
        self.d_matrices = [] # Niz koji će sadržati sve delte - matrice prelaza
        self.t_matrices = [] # Niz koji će sadržati sve tau - završne vektore

    # Funkcija koja od linije koja se pročita iz fajla napravi vektor
    def formatLineToVector(self, line):
        line = [num for num in line[:-1].split(',')] # Elementi u fajlu su međusobno odvojeni zarezima i svaka linija se završava sa \n
        i = 0
        for v in line:
            if line[i] == '+':
                line[i] = np.Inf # + označava +beskonačno
            elif line[i] == '-':
                line[i] = np.NINF # - označava -beskonačno
            else:
                line[i] = Fraction(v)
            i += 1

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
                    letter = line[-2] # uzimamo sloco koje stoji u toj liniji (-1 je \n, -2 je samo slovo)
                    i += 1  
                    matrix = np.zeros((self.n,self.n),dtype = Fraction)
                    num = 0
                    # Kako je matrica n x n dimenzija, u narednih n redova se nalazi matrica
                    for j in range(i, i+self.n):
                        row = self.formatLineToVector(lines[j])
                        matrix[num,:] = row
                        num += 1
                    i = j
                    matrix = Matrix("d_" + letter, matrix, False, 0, False)
                    self.d_matrices.append(matrix)

    # Determinizacija - Određivanje sigma vektora
    def determinisation_sigmas(self, level, fraction, type):
        for s in self.s_matrices:
            # Ukoliko smo vršili ograničenje do koje dužine reči da se vrši izračunavanje
            if s.level == level:
                break
            # Množenje vršimo isključivo ukoliko vektor s nije pretodno zatvoren i množimo ga sa svim mogućim matricama prelaza
            if s.closed != True:
                for d in self.d_matrices:
                    if type == "R♾️":
                        s_prod = s.max_plus_inf_sigma(d, self.n, fraction)
                    else:
                        s_prod = s.max_plus_sigma(d, self.n, fraction) # rezultat množenja je vektor = vektor * matrica
                    s_closed = False # Moramo proveriti da li već postoji takva matrica u nizu, i ukoliko postoji čvor proglasiti za zatvoren
                    for sp in self.s_matrices:
                        if np.array_equal(sp.value, s_prod):
                            s_closed = True
                            break

                    letter = d.name[-1] 
                    s_name = s.name + letter  # ime novog vektora dobijamo kao ime vektora i ime matrice prelaza čijim množenjem je nastao
                    s_level = len(s.name) - 1 # dužina reči vektora s
                    s_new = Matrix(s_name, s_prod, s_closed, s_level, False) # formiramo vektor u objekat
                    self.s_matrices.append(s_new) # u niz s vektora dodamo i novodobijeni

    # Determinizacija - Određivanje tau vektora
    def determinisation_taus(self, level, fraction, type):
        for t in self.t_matrices:
            # Ukoliko smo vršili ograničenje do koje dužine reči da se vrši izračunavanje
            if t.level == level:
                break
            # Množenje vršimo isključivo ukoliko vektor t nije pretodno zatvoren i množimo ga sa svim mogućim matricama prelaza
            if t.closed != True:
                for d in self.d_matrices:
                    if type == "R♾️":
                        t_prod = d.max_plus_inf_tau(t, self.n, fraction) # rezultat množenja je vektor = matrica * vektor
                    else:
                        t_prod = d.max_plus_tau(t, self.n, fraction) # rezultat množenja je vektor = matrica * vektor
                    t_closed = False # Moramo proveriti da li već postoji takva matrica u nizu, i ukoliko postoji čvor proglasiti za zatvoren
                    for tp in self.t_matrices:
                        if np.array_equal(tp.value, t_prod):
                            t_closed = True
                            break
                    
                    letter = d.name[-1]
                    t_name = "t_" + letter + t.name[2:] # ime novog vektora dobijamo kao ime matrice prelaza i ime vektora čijim množenjem je nastao
                    t_level = len(t.name) - 1 # dužina reči vektora t
                    t_new = Matrix(t_name, t_prod, t_closed, t_level, False) # formiramo vektor u objekat
                    self.t_matrices.append(t_new) # u niz t vektora dodamo i novodobijeni

    # Ispis u fajlu (inicijalna, prelazi, finalna, prosleđeni vektori)
    def print_results_in_file(self, file, vectors):
        with open(file, 'w') as f:
            f.write(self.s_matrices[0].print_vector_in_file())
            for d in self.d_matrices:
                f.write(d.print_matrix_in_file())
            f.write(self.t_matrices[0].print_vector_in_file())
            f.write("-------------------- \n")
            for v in vectors:
                f.write(v.print_vector_in_file())

    # Priprema stringova za ispis u GUI
    def print_initial_in_GUI(self):
        str = self.s_matrices[0].print_vector_in_file()
        for d in self.d_matrices:
            str += d.print_matrix_in_file()
        str += self.t_matrices[0].print_vector_in_file()
        return str
    
    def print_vectors_in_GUI(self, vectors):
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
    def nerode(self, file_name, determinisation_type, level, type):
        self.read_from_file(file_name) # učitavanje podataka iz fajla
        fraction = True # da li želimo da nam ispisuje kao razlomke ili decimale
        if determinisation_type == "Word length (decimal)":
            fraction = False
        self.determinisation_sigmas(level, fraction, type) # određivanje sigma vektora
        self.determinisation_taus(level, fraction, type) # određivanje tau vektora
        self.print_results_in_file('output1.txt', self.s_matrices) # upis sigma vektora u fajl
        self.print_results_in_file('output2.txt', self.t_matrices) # upis tau vektora u fajl
        return [self.print_vectors_in_GUI(self.s_matrices), self.print_vectors_in_GUI(self.t_matrices)] # stringovi za ispis vektora s i t u GUI