from fractions import Fraction
import emoji
import numpy as np

class Matrix:
    def __init__(self, name, value, closed, level, final) -> None:
        self.name = name # naziv matrice
        self.value = value # sama matrica
        self.closed = closed # ukoliko je čvor zatvoren vrednost je True (odnosi se na izračunavanje sigma vektora), u suprotnom je False
        self.level = level # kada kreiramo stablo, značajni su nam nivoi tj. dužine reči 
        self.final = final # ukoliko je stanje u skupu finalnih stanja vrednost je true, u suprotnom je False
    
    # Množenje dve matrice proizvod strukturom
    def multiply_matrices(self, B, e, type):
        A = self.value # A - Matrica sa leve strane
        B = B.value # B - Matrica sa desne strane
        C = np.zeros((len(A), len(B[0])), dtype = type) # C - Proizvod matrica

        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    C[i][j] = max(C[i][j], A[i][k] * B[k][j])
                    if C[i][j] < e:
                        C[i][j] = 0
        return C

    # Metoda koja štampa matricu u konzoli
    def print_matrix_in_console(self):
        closed_emoji = ""
        if self.closed:
            closed_emoji = emoji.emojize(':white_square_button:') #stop_button, white_medium_square
        print(self.name, "=", self.value, closed_emoji)

    # Metoda koja štampa matricu u fajlu
    def print_matrix_in_file(self):
        s = self.name  # s - ime matrice
        m = len(self.value) # m - broj redova
        n = len(self.value[0]) # n - broj kolona

        if m == 1 or n == 1: s = s + " = " # ako je vektor, onda iza naziva ide odmah =
        else: s = s + "\n" # ako je matrica, onda napraviti novi red, pa u novom redu ispis matrice

        if n == 1:
            self.value = np.transpose(self.value)
            m = len(self.value) # m - broj redova
            n = len(self.value[0]) # n - broj kolona
            
        for i in range(0, m):
            for j in range(0, n):
                s = s + str(self.value[i][j]) + " "
                
            closed_emoji = ""
            if self.closed:
                closed_emoji = emoji.emojize(':white_square_button:') # ukoliko je zatvoren, staviti emotikon

            s += closed_emoji + "\n"

        if n == 1:
            self.value = np.transpose(self.value)
        
        return s


    