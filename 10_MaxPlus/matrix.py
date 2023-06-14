from fractions import Fraction
import emoji
import numpy as np

class Matrix:
    def __init__(self, name, value, closed, level, final) -> None:
        self.name = name # naziv matrice
        self.value = value # sama matrica
        self.closed = closed # ukoliko je čvor zatvoren vrednost je True, u suprotnom je False
        self.level = level # nivoi tj. dužina reči 
        self.final = final # ukoliko je stanje u skupu finalnih stanja vrednost je true, u suprotnom je False

    # Metoda za kreiranje prazne Max-Plus matrice
    def empty_matrix(self, n, fraction):
        # Definišemo tip matrice i njene dimenzije
        if fraction:
            C = np.zeros((1, n),dtype = Fraction)[0]
        else:
            C = np.zeros((1, n),dtype = float)[0]

        # Matricu popunimo najmanjim mogućim elementom a to je -besk.
        for i in range(0, n):
            for j in range(0, n):
                C[i] = np.NINF
        return C

    # Metoda za R max-plus strukturu za sigme tj. množenje vektor * matrica u max-plus
    def max_plus_sigma(self, B, n, fraction):  
        A = self.value # Sigma vektor
        B = B.value # Matrica
        C = self.empty_matrix(n, fraction)

        # a + b = max(a,b)
        # a x b = a + b (za a i b iz R) / -besk. (za a=-besk. ili b=-besk.)
        for i in range(0, n):
            for j in range(0, n):
                if A[j]==np.NINF or A[j]==np.Inf or B[j][i]==np.NINF or B[j][i]==np.Inf:
                    C[i] = max(C[i], np.NINF)
                else:
                    C[i] = max(C[i], A[j] + B[j][i])
        return C

    # Metoda za R max-plus strukturu za tau tj. množenje matrica * vektor
    def max_plus_tau(self, B, n, fraction):  
        A = self.value # matrica
        B = B.value # T vektor
        C = self.empty_matrix(n, fraction)

        # a + b = max(a,b)
        # a x b = a + b (za a i b iz R) / -besk. (za a=-besk. ili b=-besk.)
        for i in range(0, n):
            for j in range(0, n):
                if A[i][j]==np.NINF or A[i][j]==np.Inf or B[j]==np.NINF or B[j]==np.Inf:
                    C[i] = max(C[i], np.NINF)
                else:
                    C[i] = max(C[i], A[i][j] + B[j])
        return C

    # Metoda za R inf. max-plus strukturu za sigme tj. množenje vektor * matrica u inf. max-plus
    def max_plus_inf_sigma(self, B, n, fraction):  
        A = self.value # Sigma vektor
        B = B.value # Matrica
        C = self.empty_matrix(n, fraction)

        # a + b = max(a,b)
        # a x b = a + b (za a i b iz R) / -besk. ako je sa leve ili desne strane -besk. / +besk. u ostalim slučajevima
        for i in range(0, n):
            for j in range(0, n):
                if A[j]==np.NINF or B[j][i]==np.NINF:
                    C[i] = C[i] # Maks. između bilo čeha i -beskonačnog je to nešto
                elif A[j]==np.Inf or B[j][i]==np.Inf:
                    C[i] = np.Inf # Maks. između bilo čega i beskonačnog je beskonačno
                else:
                    C[i] = max(C[i], A[j] + B[j][i])
        return C

    # Metoda za R inf. max-plus strukturu za tau tj. množenje matrica * vektor u inf. max-plus
    def max_plus_inf_tau(self, B, n, fraction):  
        A = self.value # matrica
        B = B.value # T vektor
        C = self.empty_matrix(n, fraction)

        # a + b = max(a,b)
        # a x b = a + b (za a i b iz R) / -besk. ako je sa leve ili desne strane -besk. / +besk. u ostalim slučajevima
        for i in range(0, n):
            for j in range(0, n):
                if A[i][j]==np.NINF or B[j]==np.NINF:
                    C[i] = C[i] # Maks. između bilo čeha i -beskonačnog je to nešto
                elif A[i][j]==np.Inf or B[j]==np.Inf:
                    C[i] = np.Inf # Maks. između bilo čega i beskonačnog je beskonačno
                else:
                    C[i] = max(C[i], A[i][j] + B[j])
        return C

    def res(self, a, b):
        if b == np.Inf or a == np.NINF:
            c = np.Inf
        elif a != np.Inf and a != np.NINF and b != np.Inf and b != np.NINF:
            c = b - a
        else:
            c = np.NINF
        return c

    def right(self, A, B):
        if len(A) == len(B):
            c_n = len(A[0])
            c_m = len(B[0])
            C = np.Inf(c_n, c_m, dtype = Fraction)
            for j in range(c_n):
                for k in range(c_m):
                    for i in range(len(A)):
                        C[j][k] = min(C[j][k], self.res(A[i][j], B[i][k]))
        else:
            print("Error")

    def left(self, A, B):
        if len(A[0]) == len(B[0]):
            c_n = len(B) # m
            c_m = len(A) # n
            C = np.Inf(c_n, c_m, dtype = Fraction) # m x n
            for i in range(c_n):
                for j in range(c_m):
                    for k in range(len(A[0])):
                        C[i][j] = min(C[i][j], self.res(A[j][k], B[i][k]))
        else:
            print("Error")

    # Metoda koja priprema štampanje matrice u konzoli
    def print_matrix_in_console(self):
        closed_emoji = ""
        if self.closed:
            closed_emoji = emoji.emojize(':white_square_button:') 
        print(self.name, "=", self.value, closed_emoji)

    # Metoda koja priprema štampanje vektora u fajlu
    def print_vector_in_file(self):
        vector = self.name + " = "
        n = len(self.value)
        for i in range(0, n):
            vector = vector + str(self.value[i]) + " "

        closed_emoji = ""
        if self.closed:
            closed_emoji = emoji.emojize(':white_square_button:') 
        vector += closed_emoji + "\n"
        return vector

    # Metoda koja priprema štampanje matrice u fajlu
    def print_matrix_in_file(self):
        matrix = self.name + "\n"
        m = len(self.value)
        n = len(self.value[0])
        for i in range(0, m):
            for j in range(0, n):
                matrix = matrix + str(self.value[i][j]) + " "
            matrix = matrix + "\n"
        return matrix