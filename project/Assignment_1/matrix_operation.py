from typing import List


def addition_matrices(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:

    if len(matrix1) == len(matrix2) and (len(matrix1[0]) == len(matrix2[0])):
        return [
            [matrix1[i][j] for i in range(len(matrix1[0]))] for j in range(len(matrix1))
        ]
    raise ValueError("Matrices must have same dimensions")


def multiplication_matrices(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    if len(matrix1[0]) == len(matrix2):
        return [
            [
                sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix1[0])))
                for j in range(len(matrix2[0]))
            ]
            for i in range(len(matrix1))
        ]
    raise ValueError("Matrices must have correct dimensions")


def transpose(matrix1: List[List[float]]) -> List[List[float]]:
    return [
        [matrix1[j][i] for j in range(len(matrix1))] for i in range(len(matrix1[0]))
    ]
