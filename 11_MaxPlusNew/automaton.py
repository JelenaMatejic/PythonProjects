from matrix import Matrix
import utility

class Automaton:
    def __init__(self, filepath):
        self.n = None
        self.sigma = None
        self.tau = None
        self.transitions = []

        self.read_file(filepath)

    def read_file(self, filepath):
        with open(filepath, 'r') as file:
            # Read the entire file
            lines = file.readlines()

            # Remove newline characters from each line and filter out empty lines
            lines = [line.strip() for line in lines if line.strip()]

            # Check if the file format is valid
            if len(lines) < 7 or lines[0] != 'states' or lines[2] != 'start' or lines[4] != 'end':
                print('Invalid file format')
                return

            # Read the number of states
            self.n = int(lines[1])

            # Read the start vector
            start_vector = [Automaton.parse_value(x) for x in lines[3].split(',')]
            self.sigma = Matrix('start', [start_vector])

            # Read the end vector
            end_vector = [Automaton.parse_value(x) for x in lines[5].split(',')]
            self.tau = Matrix('end', [end_vector])
            # self.tau.transpose()

            # Read the transitions
            current_transition = None
            for line in lines[6:]:
                if line.startswith('transition'):
                    current_transition = line.split(' ')[1][-1]
                    matrix = Matrix(current_transition, [[]])
                    matrix.value = []
                    matrix.rows = 0
                    self.transitions.append(matrix)
                else:
                    if current_transition is not None:
                        row = [Automaton.parse_value(x) for x in line.split(',')]
                        matrix.value.append(row)
                        matrix.rows += 1
                        matrix.cols = len(row)

    def parse_value(value):
        if value == '-' or value == '-inf':
            return float('-inf')
        elif value == '+' or value == 'inf':
            return float('inf')
        else:
            return float(value)

    def print_automaton(self):
        print('Number of states:', self.n)
        print('Start vector:')
        self.sigma.print_matrix()
        print('End vector:')
        self.tau.print_matrix()
        for transition, matrix in self.transitions.items():
            print('Transition ', transition)
            matrix_obj = Matrix(transition, matrix)
            matrix_obj.print_matrix()

    def print_automaton_in_file(self, file):
        self.clear_file(file)
        self.sigma.print_matrix_in_file(file)
        self.tau.print_matrix_in_file(file)
        for transition, matrix in self.transitions.items():
            matrix_obj = Matrix(transition, matrix)
            matrix_obj.print_matrix_in_file(file)
    
    def clear_file(self, file):
        with open(file, 'w') as file:
            file.write('')

