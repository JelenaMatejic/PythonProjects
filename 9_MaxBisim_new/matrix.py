from cmath import inf

class Matrix:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.rows = len(self.value)
        self.cols = len(self.value[0])

    def transpose(self):
        value_tmp = [[self.value[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(self.name, value_tmp)

    def print_matrix(self):
        print(self.name)
        for row in self.value:
            print(','.join(str(element) for element in row))
        print("---------------")

    def print_matrix_in_file(self, filepath):
        with open(filepath, 'a') as file:
            file.write(format(self.name) + '\n')
            for row in self.value:
                file.write(','.join(str(element) for element in row) + '\n')