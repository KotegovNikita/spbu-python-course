import random


class Dice:
    """Represents a single six-sided die."""

    def __init__(self) -> None:
        """Initializes the die with a random value between 1 and 6."""
        self.value: int = random.randint(1, 6)

    def roll(self) -> None:
        """Rolls the die and updates its value to a new random number."""
        self.value = random.randint(1, 6)

    def __str__(self) -> str:
        """Returns the string representation of the die's current value."""
        return str(self.value)

    def __repr__(self) -> str:
        """Returns the detailed representation of the die object."""
        return f"Dice({self.value})"
