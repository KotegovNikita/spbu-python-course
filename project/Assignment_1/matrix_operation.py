from typing import List


def addition_matrices(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """
    Add two matrices

    Parameters:
        matrix_a (List[List[float]]): First matrix
        matrix_b (List[List[float]]): Second matrix

    Returns:
        Optional[List[List[float]]]: Sum of matrix a and matrix b
    """
    if not matrix1 or not matrix1[0] or not matrix2 or not matrix2[0]:
        raise ValueError("Matrices must not be empty")

    if len(matrix1) == len(matrix2) and (len(matrix1[0]) == len(matrix2[0])):
        return [
            [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
            for i in range(len(matrix1))
        ]
    raise ValueError("Matrices must have same dimensions")


def multiplication_matrices(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """
    Multiplicate two matrices

    Parameters:
        matrix_a (List[List[float]]): First matrix
        matrix_b (List[List[float]]): Second matrix

    Returns:
        Optional[List[List[float]]]: Product of matrix a and matrix b
    """
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
    """
     Transpose a matrix

    Parameters:
        matrix (List[List[float]]): Matrix

    Returns:
        Optional[List[List[float]]]: Transposed matrix
    """
    if not matrix1:
        return []
    return [
        [matrix1[j][i] for j in range(len(matrix1))] for i in range(len(matrix1[0]))
    ]
