import pytest
from project.Assignment_1.matrix_operation import (
    addition_matrices,
    multiplication_matrices,
    transpose,
)


def test_addition_valid_2x2():
    """
    Test matrix addition with two 2x2 matrices.

    Verifies the operation returns the correct element-wise sum.

    Test cases:
    - Basic 2x2 matrices (float values).
    """
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    expected = [[6.0, 8.0], [10.0, 12.0]]
    assert addition_matrices(A, B) == expected


def test_addition_invalid_dimensions():
    """
    Test matrix addition with incompatible dimensions.

    Verifies that the function raises a ValueError when dimensions don't match.

    Test cases:
    - Matrix 1x2 and Matrix 2x1.
    """
    A = [[1.0, 2.0]]  # 1x2
    B = [[5.0], [7.0]]  # 2x1
    with pytest.raises(ValueError) as excinfo:
        addition_matrices(A, B)
    assert "same dimensions" in str(excinfo.value)


def test_multiplication_valid_2x2_by_2x2():
    """
    Test matrix multiplication for two 2x2 square matrices.

    Verifies the correct matrix product is returned.

    Test cases:
    - Basic 2x2 matrices.
    """
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    expected = [[19.0, 22.0], [43.0, 50.0]]
    assert multiplication_matrices(A, B) == expected


def test_multiplication_valid_2x3_by_3x2():
    """
    Test matrix multiplication for compatible non-square matrices.

    Verifies A(2x3) * B(3x2) returns a C(2x2) matrix.

    Test cases:
    - Matrix 2x3 and Matrix 3x2.
    """
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    B = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
    expected = [[58.0, 64.0], [139.0, 154.0]]
    assert multiplication_matrices(A, B) == expected


def test_multiplication_invalid_dimensions():
    """
    Test matrix multiplication with incompatible dimensions.

    Verifies that a ValueError is raised when columns(A) != rows(B).

    Test cases:
    - Matrix 1x2 and Matrix 1x2.
    """
    A = [[1.0, 2.0]]  # 1x2
    B = [[3.0, 4.0]]  # 1x2
    with pytest.raises(ValueError) as excinfo:
        multiplication_matrices(A, B)
    assert "correct dimensions" in str(excinfo.value)


# --- Тесты для transpose ---


def test_transpose_square():
    """
    Test transposition for a square 2x2 matrix.

    Verifies rows and columns are correctly swapped.

    Test cases:
    - Basic 2x2 matrix.
    """
    A = [[1.0, 2.0], [3.0, 4.0]]
    expected = [[1.0, 3.0], [2.0, 4.0]]
    assert transpose(A) == expected


def test_transpose_rectangular():
    """
    Test transposition for a rectangular matrix.

    Verifies a 2x3 matrix is correctly transposed to a 3x2 matrix.

    Test cases:
    - Basic 2x3 matrix.
    """
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    expected = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    assert transpose(A) == expected


def test_transpose_vector_row():
    """
    Test transposition of a row vector.

    Verifies a 1x3 row vector is correctly converted to a 3x1 column vector.

    Test cases:
    - Single row vector (1x3).
    """
    A = [[1.0, 2.0, 3.0]]
    expected = [[1.0], [2.0], [3.0]]
    assert transpose(A) == expected
