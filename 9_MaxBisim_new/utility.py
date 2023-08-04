from cmath import inf
from matrix import Matrix

def multiply(matrix_m, matrix_n, epsilon):
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
                    element = max(element, a*b)
                if(element < epsilon):
                    element = 0
                row.append(element)
            result.append(row)
        
        return Matrix("Result", result)

def min_matrix(matrix_m, matrix_n):
    matrix_res = matrix_m
    for i in range(matrix_n.rows):
        for j in range(matrix_n.cols):
            matrix_res.value[i][j] = min(matrix_res.value[i][j], matrix_n.value[i][j])
    return matrix_res

def findByKey(arr, key):
        for item in arr:
            if item.get("word") == key:
                return item.get("vector")
        return False

def findByValue(arr, value):
    keys = []
    for item in arr:
        if item.get("vector").value == value:
            x = item.get("word")
            keys.append(x)
    if not keys:
        return False
    else:
        return keys

def compareArrays(arr1, arr2):
    for a1 in arr1:
        for a2 in arr2:
            if a1 == a2:
                return True
    return False

