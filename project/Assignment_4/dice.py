# dice.py
import random


class Dice:
    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        self.value = random.randint(1, 6)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Dice({self.value})"
