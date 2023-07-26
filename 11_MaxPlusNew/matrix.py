from cmath import inf
import re
import numpy as np

class Matrix:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.rows = len(self.value)
        self.cols = len(self.value[0])

    def transpose(self):
        value_tmp = [[self.value[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(self.name + "^T", value_tmp)

    def print_matrix(self):
        print(self.name)
        for row in self.value:
            print(','.join(str(element) for element in row))
        print("---------------")
        
    @staticmethod
    def convert_inf_to_str(data):
        if isinstance(data, list):
            return [Matrix.convert_inf_to_str(item) for item in data]
        return str(data) if data == -float('inf') or data == float('inf') else data 

    def get_matrix(self):
        my_dict =  self.__dict__.copy()
        my_dict['value'] = Matrix.convert_inf_to_str(my_dict['value'])
        return my_dict

    def print_matrix_in_file(self, filepath):
        with open(filepath, 'a') as file:
            file.write(format(self.name) + '\n')
            for row in self.value:
                file.write(','.join(str(element) for element in row) + '\n')

# for i in range(m_cols):
#     for j in range(n_cols):
#         column_m = [row[i] for row in matrix_m.value]
#         column_n = [row[j] for row in matrix_n.value]
#         for a, b in zip(column_m, column_n):
#             result[i][j] = min(result[i][j], self.residual(a, b))