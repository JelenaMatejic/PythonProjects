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
    
    # Metoda za klasično množenje dve matrice
    def multiply_matrix(self, A, B, n):   
        C = np.zeros((1, n),dtype = Fraction)
        C = np.matmul(A, B)
        return C

    # Metoda za product strukturu ali bez E ograničenja
    def product_structure_matrix(self, B, n):  
        A = self.value
        B = B.value
        C = np.zeros((1, n),dtype = Fraction)[0]

        # + operator zamenjen sa max
        for i in range(0, n):
            for j in range(0, n):
                C[i] = max(C[i], A[j] * B[j][i])
        return C

    # Metoda za product strukturu ali sa E ograničenjem
    def product_structure_matrix_bounded(self, B, n):  
        A = self.value
        B = B.value
        C = np.zeros((1, n),dtype = Fraction)[0]

        # + operator zamenjen sa max
        for i in range(0, n):
            for j in range(0, n):
                C[i] = max(C[i], A[j] * B[j][i])
            # Ako smo dobili rezultat ispod 0.01, postavimo ga na 0
            if C[i] < 0.01:
                C[i] = 0
        return C

    # Metoda koja štampa matricu u konzoli
    def print_matrix_in_console(self):
        closed_emoji = ""
        if self.closed:
            closed_emoji = emoji.emojize(':white_square_button:') #stop_button, white_medium_square
        print(self.name, "=", self.value, closed_emoji)

    # Metoda koja štampa vektor u fajlu
    def print_vector_in_file(self):
        n = len(self.value)

        s = self.name + " = "
        for i in range(0, n):
            s = s + str(self.value[i]) + " "

        closed_emoji = ""
        if self.closed:
            closed_emoji = emoji.emojize(':white_square_button:') #stop_button, white_medium_square
            
        s += closed_emoji + "\n"
        return s

    # Metoda koja štampa matricu u fajlu
    def print_matrix_in_file(self):
        s = self.name + "\n"
        m = len(self.value)
        n = len(self.value[0])
        for i in range(0, m):
            for j in range(0, n):
                s = s + str(self.value[i][j]) + " "
            s = s + "\n"
        return s