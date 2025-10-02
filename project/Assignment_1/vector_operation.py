from math import acos, pi
from typing import List, Optional


def scalar_multiplication_of_vectors(
    vector1: List[float], vector2: List[float]
) -> Optional[float]:
    """
    Calculate scalar product of two vectors

    Parameters:
        vector1 (List[float]): First vector
        vector2 (List[float]): Second vector

    Returns:
        Optional[float]: Scalar product of vectors vector1 and vector2
    """
    if len(vector1) == len(vector2):
        return sum([vector1[i] * vector2[i] for i in range(len(vector1))])
    raise ValueError("Vectors must have same dimensions")


def find_length_of_vectors(vector1: List[float]) -> Optional[float]:
    """
    Calculate length of a vector

    Parameters:
        vector (List[float]): Input vector

    Returns:
        float: Length of vector
    """
    return sum([vector1[i] ** 2 for i in range(len(vector1))]) ** 0.5


def get_angle_between_vectors(
    vector1: List[float], vector2: List[float]
) -> Optional[float]:
    """
    Calculate angle between two vectors

    Parameters:
        vector1 (List[float]): First vector
        vector2 (List[float]): Second vector

    Returns:
        Optional[float]: Angle between vectors in radians
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors sizes must be equal")

    return (
        180
        * acos(
            scalar_multiplication_of_vectors(vector1, vector2)
            / (find_length_of_vectors(vector1) * find_length_of_vectors(vector2))
        )
        / pi
    )
