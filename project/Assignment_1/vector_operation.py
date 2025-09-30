from math import sqrt, acos
from typing import List, Optional


def scalar_multiplication_of_vectors(
    vector1: List[float], vector2: List[float]
) -> Optional[float]:
    if len(vector1) == len(vector2):
        return sum([vector1[i] * vector2[i] for i in range(len(vector1))])
    raise ValueError("Vectors must have same dimensions")


def find_length_of_vectors(vector1: List[float]) -> Optional[float]:
    return sum([vector1[i] ** 2 for i in range(len(vector1))]) ** 0.5


def get_angle_between_vectors(
    vector1: List[float], vector2: List[float]
) -> Optional[float]:
    if len(vector1) == len(vector2):
        scalar = scalar_multiplication_of_vectors(vector1, vector2)
        length1 = find_length_of_vectors(vector1)
        length2 = find_length_of_vectors(vector2)

        denominator = length1 * length2
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")

        cos_angle = scalar / denominator
        return acos(cos_angle)
    raise ValueError("Vectors must have same dimensions")
