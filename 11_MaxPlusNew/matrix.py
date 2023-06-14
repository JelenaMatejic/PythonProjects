from cmath import inf

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
        for row in self.value:
            print(','.join(str(element) for element in row))
        print("---------------")

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