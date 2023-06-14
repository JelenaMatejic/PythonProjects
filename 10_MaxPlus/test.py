from dataclasses import asdict
from hashlib import new
import tkinter as tk
from matplotlib import projections
import numpy as np
from traceback import print_tb
from matrix import Matrix
from fractions import Fraction

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

# Niz koji će sadržati sve matrice za bisimulacije
t_matrices_bisim = []

def formatLineToVector(line):
        line = [num for num in line[:-1].split(',')] # elementi u fajlu su međusobno odvojeni zarezima
        i = 0
        for v in line:
            if v == '+':
                line[i] = np.Inf
            elif line[i] == '-':
                line[i] = np.NINF
            else:
                line[i] = Fraction(v)
            i += 1

        vector = np.array(line)
        return vector

file = open("example_4_2.txt", "r")
with file:
    # Pročitaćemo ceo fajl, a onda se kretati liniju po liniju u njemu
    lines = file.readlines() 
    for i in range(0, len(lines)):
        line = lines[i]
        # Ako pročita reč "states", to znači da se u narednom redu (i += 1) nalazi broj stanja automata
        if "states" in line:
            i += 1
            line = lines[i]
            n = int(line)

        # Ako pročita reč "start", to znači da se u narednom redu (i += 1) nalazi vektor inicijalnih stanja automata
        elif "start" in line:
            i += 1
            s = formatLineToVector(lines[i]) # od pročitane linije napravimo vektor
            matrix = Matrix("s_", s, False, 0, False) # pošto je ovo vektor/matrica početnih stanja, kreiramo objekat klase Matrix
            s_matrices.append(matrix) # dodamo inicijalnu matricu u skup svih sigma matrica
            s_matrices_e.append(matrix) # dodamo inicijalnu matricu u skup svih sigma matrica

        # Ako pročita reč "end", to znači da se u narednom redu (i += 1) nalazi vektor finalnih stanja automata
        elif "end" in line:
            i += 1  
            t = formatLineToVector(lines[i]) # od pročitane linije napravimo vektor
            matrix = Matrix("t_", t, False, 0, True) # pošto je ovo vektor/matrica početnih stanja, kreiramo objekat klase Matrix
            t_matrices.append(matrix)
            t_matrices_e.append(matrix)
        
        # Ako pročita reč transition, to znači da se u narednim redovima nalaze matrice prelaza za dati automat
        elif "transition" in line:
            letter = line[-2]
            i += 1  
            matrix = np.zeros((n,n))
            num = 0
            for j in range(i, i+n):
                row = formatLineToVector(lines[j])
                matrix[num,:] = row
                num += 1
            i = j
            matrix = Matrix("d_" + letter, matrix, False, 0, False)
            d_matrices.append(matrix)

s_matrices[0].print_matrix_in_console()
t_matrices[0].print_matrix_in_console()
d_matrices[0].print_matrix_in_console()
d_matrices[1].print_matrix_in_console()