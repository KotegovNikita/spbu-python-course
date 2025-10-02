import pytest
from math import pi, sqrt, isclose
from project.Assignment_1.vector_operation import (
    scalar_multiplication_of_vectors,
    find_length_of_vectors,
    get_angle_between_vectors,
)


# ----------------------------------------------------------------------
# Тесты для scalar_multiplication_of_vectors
# ----------------------------------------------------------------------


def test_scalar_multiplication_valid_2d():
    """
    Test the scalar (dot) product for 2D vectors.

    Verifies the correct scalar result for two basic vectors.

    Test cases:
    - Vectors [1, 3] and [2, 4].
    """
    v1 = [1.0, 3.0]
    v2 = [2.0, 4.0]
    expected = 1 * 2 + 3 * 4  # 2 + 12 = 14
    assert scalar_multiplication_of_vectors(v1, v2) == expected


def test_scalar_multiplication_valid_3d():
    """
    Test the scalar product for 3D vectors.

    Verifies the correct scalar result for two 3D vectors including negative components.

    Test cases:
    - Vectors [5, -2, 1] and [0, 3, 10].
    """
    v1 = [5.0, -2.0, 1.0]
    v2 = [0.0, 3.0, 10.0]
    expected = 5 * 0 + (-2) * 3 + 1 * 10  # 0 - 6 + 10 = 4
    assert scalar_multiplication_of_vectors(v1, v2) == expected


def test_scalar_multiplication_orthogonal():
    """
    Test the scalar product for orthogonal vectors.

    Verifies the result is 0.0 for two perpendicular vectors.

    Test cases:
    - Orthogonal vectors [1, 0] and [0, 5].
    """
    v1 = [1.0, 0.0]
    v2 = [0.0, 5.0]
    expected = 0.0
    assert scalar_multiplication_of_vectors(v1, v2) == expected


def test_scalar_multiplication_invalid_dimensions():
    """
    Test the scalar product error handling for mismatched dimensions.

    Verifies a ValueError is raised when dimensions are unequal.

    Test cases:
    - Vector 2D and Vector 3D.
    """
    v1 = [1.0, 2.0]
    v2 = [3.0, 4.0, 5.0]
    with pytest.raises(ValueError) as excinfo:
        scalar_multiplication_of_vectors(v1, v2)
    assert "same dimensions" in str(excinfo.value)


# ----------------------------------------------------------------------
# Тесты для find_length_of_vectors
# ----------------------------------------------------------------------


def test_find_length_2d_basic():
    """
    Test the calculation of the Euclidean norm (length) for a 2D vector.

    Verifies the correct length for a Pythagorean triple vector.

    Test cases:
    - Vector [3, 4].
    """
    v = [3.0, 4.0]
    expected = 5.0
    assert find_length_of_vectors(v) == expected


def test_find_length_3d_complex():
    """
    Test the calculation of the length for a 3D vector.

    Verifies the correct square root result is returned.

    Test cases:
    - Vector [1, 1, 1].
    """
    v = [1.0, 1.0, 1.0]
    expected = sqrt(3)
    assert find_length_of_vectors(v) == pytest.approx(expected)


def test_find_length_zero_vector():
    """
    Test the length calculation for the zero vector.

    Verifies the length is zero.

    Test cases:
    - Vector [0, 0, 0].
    """
    v = [0.0, 0.0, 0.0]
    expected = 0.0
    assert find_length_of_vectors(v) == expected


# ----------------------------------------------------------------------
# Тесты для get_angle_between_vectors
# ----------------------------------------------------------------------


def test_get_angle_opposite_direction():
    """
    Test angle calculation for anti-parallel vectors.

    Verifies the angle is $\pi$ radians (180 degrees).

    Test cases:
    - Opposite vectors [1, 0] and [-1, 0].
    """
    v1 = [1.0, 0.0]
    v2 = [-1.0, 0.0]
    expected = pi
    assert get_angle_between_vectors(v1, v2) == pytest.approx(expected)


def test_get_angle_orthogonal():
    """
    Test angle calculation for orthogonal vectors.

    Verifies the angle is $\pi/2$ radians (90 degrees).

    Test cases:
    - Orthogonal vectors [1, 0] and [0, 1].
    """
    v1 = [1.0, 0.0]
    v2 = [0.0, 1.0]
    expected = pi / 2
    assert get_angle_between_vectors(v1, v2) == pytest.approx(expected)


def test_get_angle_45_degrees():
    """
    Test angle calculation for a 45-degree angle.

    Verifies the angle is $\pi/4$ radians.

    Test cases:
    - Vectors [1, 0] and [1, 1].
    """
    v1 = [1.0, 0.0]
    v2 = [1.0, 1.0]
    expected = pi / 4
    assert get_angle_between_vectors(v1, v2) == pytest.approx(expected)


def test_get_angle_invalid_dimensions():
    """
    Test angle calculation error handling for mismatched dimensions.

    Verifies a ValueError is raised when dimensions are unequal.

    Test cases:
    - Vector 2D and Vector 3D.
    """
    v1 = [1.0, 2.0]
    v2 = [3.0, 4.0, 5.0]
    with pytest.raises(ValueError) as excinfo:
        get_angle_between_vectors(v1, v2)
    assert "same dimensions" in str(excinfo.value)


def test_get_angle_with_zero_vector():
    """
    Test angle calculation error when one vector is the zero vector.

    Verifies a ValueError is raised due to zero denominator.

    Test cases:
    - Vector [1, 2] and zero vector [0, 0].
    """
    v1 = [1.0, 2.0]
    v2 = [0.0, 0.0]
    with pytest.raises(ValueError) as excinfo:
        get_angle_between_vectors(v1, v2)
    assert "Denominator cannot be zero" in str(excinfo.value)
