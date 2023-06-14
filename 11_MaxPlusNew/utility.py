from cmath import inf
from matrix import Matrix

def multiply(matrix_m, matrix_n):
        # Matrix M of dimensions m x n
        # Matrix N of dimensions n x p
        # Matrix M * N dimensin m x p

        if matrix_m.cols != matrix_n.rows:
            raise ValueError("The number of columns in the first matrix must match the number of rows in the second matrix.")
        
        result = []
        for i in range(matrix_m.rows):
            row = []
            for j in range(matrix_n.cols):
                element = -inf
                for k in range(matrix_n.rows):
                    a = matrix_m.value[i][k]
                    b = matrix_n.value[k][j]
                    element = max(element, times(a, b))
                row.append(element)
            result.append(row)
        
        return Matrix("Result", result)

def right_residual(matrix_m, matrix_n):
        # Matrix M of dimensions m x n
        # Matrix N of dimensions m x p
        # Matrix M\N dimensin n x p
        
        if matrix_m.rows != matrix_n.rows:
            raise ValueError("The number of rows in the first matrix must match the number of rows in the second matrix.")

        result = [[inf] * matrix_n.cols for _ in range(matrix_m.cols)] 

        for j in range(matrix_m.cols):
                for k in range(matrix_n.cols):
                    for i in range(matrix_m.rows):
                        a = matrix_m.value[i][j]
                        b = matrix_n.value[i][k]
                        result[j][k] = min(result[j][k], residual(a, b))

        return Matrix('Right Residual', result)

def left_residual(matrix_n, matrix_m):
    # Matrix N of dimensions m x p
    # Matrix M of dimensions n x p
    # Matrix N/M dimensin m x n = M -> N

    if matrix_n.cols != matrix_m.cols:
        raise ValueError("The number of rows in the first matrix must match the number of rows in the second matrix.")

    result = [[inf] * matrix_m.rows for _ in range(matrix_n.rows)] 

    for i in range(matrix_n.rows):
            for j in range(matrix_m.rows):
                for k in range(matrix_m.cols):
                    m = matrix_m.value[j][k]
                    n = matrix_n.value[i][k]
                    result[i][j] = min(result[i][j], residual(m, n))

    return Matrix('Right Residual', result)

def matrix_min(matrix_n, matrix_m):
    # Matrix N of dimensions n x m
    # Matrix M of dimensions n x m
    if matrix_n.cols != matrix_m.cols or matrix_n.rows != matrix_m.rows:
        raise ValueError("The number of rows and cols in the first matrix must match the number of rows and cols in the second matrix.")

    result = [[inf] * matrix_n.cols for _ in range(matrix_n.rows)] 

    for i in range(matrix_n.rows):
        for j in range(matrix_n.cols):
            result[i][j] = min(matrix_n.value[i][j], matrix_m.value[i][j])

    return Matrix('matrix_min', result)

def times(a, b):
    if a == -inf or b == -inf:
        return -inf
    elif a == inf or b == inf:
        return inf
    else:
        return a + b

def residual(a, b):
    if a == -inf or b == inf:
        return inf
    elif a == inf or b == -inf:
        return -inf
    else:
        return b - a