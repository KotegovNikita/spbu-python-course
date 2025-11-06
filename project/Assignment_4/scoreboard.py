from typing import List, Dict, Optional
from collections import Counter
from enum import Enum


class Category(Enum):
    """All scoring categories in the game."""

    ONES = "ones"
    TWOS = "twos"
    THREES = "threes"
    FOURS = "fours"
    FIVES = "fives"
    SIXES = "sixes"

    PAIR = "pair"
    TWO_PAIRS = "two_pairs"
    THREE_OF_A_KIND = "three_of_a_kind"
    FOUR_OF_A_KIND = "four_of_a_kind"
    SMALL_STRAIGHT = "small_straight"
    LARGE_STRAIGHT = "large_straight"
    EVEN = "even"
    ODD = "odd"
    FULL_HOUSE = "full_house"
    POKER = "poker"
    CHANCE = "chance"


class DiceValue(Enum):
    """Possible values on a six-sided die."""

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


class CombinationThreshold(Enum):
    """Minimum dice counts required for various combinations."""

    PAIR = 2
    THREE_OF_A_KIND = 3
    FOUR_OF_A_KIND = 4
    FULL_HOUSE_THREE = 3
    FULL_HOUSE_TWO = 2
    POKER = 5


class Bonus(Enum):
    """Bonus points and multipliers in the game."""

    STAGE_ONE_BONUS = 50
    POKER_BONUS = 50
    FIRST_THROW_MULTIPLIER = 2


class SmallStraight(Enum):
    """Valid small straight combinations."""

    STRAIGHT_1 = frozenset({1, 2, 3, 4})
    STRAIGHT_2 = frozenset({2, 3, 4, 5})
    STRAIGHT_3 = frozenset({3, 4, 5, 6})


class LargeStraight(Enum):
    """Valid large straight combinations."""

    STRAIGHT_1 = frozenset({1, 2, 3, 4, 5})
    STRAIGHT_2 = frozenset({2, 3, 4, 5, 6})


class Scoreboard:
    """Manages scoring for all categories in a Yahtzee game."""

    STAGE_1: List[Category] = [
        Category.ONES,
        Category.TWOS,
        Category.THREES,
        Category.FOURS,
        Category.FIVES,
        Category.SIXES,
    ]
    STAGE_2: List[Category] = [
        Category.PAIR,
        Category.TWO_PAIRS,
        Category.THREE_OF_A_KIND,
        Category.FOUR_OF_A_KIND,
        Category.SMALL_STRAIGHT,
        Category.LARGE_STRAIGHT,
        Category.EVEN,
        Category.ODD,
        Category.FULL_HOUSE,
        Category.POKER,
        Category.CHANCE,
    ]
    CATEGORIES: List[Category] = STAGE_1 + STAGE_2

    def __init__(self) -> None:
        """Initializes an empty scoreboard with all categories unfilled."""
        self.scores: Dict[Category, Optional[int]] = {c: None for c in self.CATEGORIES}

    def get_available_categories(self) -> List[Category]:
        """
        Returns all categories that haven't been filled yet.
        Returns:
            List of unfilled categories.
        """
        return [c for c, v in self.scores.items() if v is None]

    def get_stage_one_subtotal(self) -> int:
        """
        Calculates the sum of all stage one category scores.

        Returns:
            Total points from stage one categories.
        """
        return sum(
            v for c, v in self.scores.items() if c in self.STAGE_1 and v is not None
        )

    def is_complete(self) -> bool:
        """
        Checks if all categories have been filled.

        Returns:
            True if scoreboard is complete, False otherwise.
        """
        return all(v is not None for v in self.scores.values())

    def get_total_score(self) -> int:
        """
        Calculates the final score including bonuses.

        Returns:
            Total score with stage one bonus if applicable.
        """
        stage_one_total = self.get_stage_one_subtotal()
        stage_two_total = sum(
            v for c, v in self.scores.items() if c in self.STAGE_2 and v is not None
        )
        bonus = Bonus.STAGE_ONE_BONUS.value if stage_one_total >= 0 else 0
        return stage_one_total + stage_two_total + bonus

    def fill_category(
        self, category: Category, dice_values: List[int], first_throw: bool = False
    ) -> int:
        """
        Fills a category with the calculated score.

        Args:
            category: The category to fill.
            dice_values: The dice values to score.
            first_throw: Whether this was achieved on the first roll.

        Returns:
            The points earned for this category.

        Raises:
            ValueError: If category is invalid or already filled.
        """
        if category not in self.CATEGORIES:
            raise ValueError(f"Unknown category: {category}")
        if self.scores[category] is not None:
            raise ValueError(f"Category '{category.value}' is already filled")

        score = Scoreboard.score_for_category(category, dice_values, first_throw)
        self.scores[category] = score
        return score

    @staticmethod
    def score_for_category(
        category: Category, dice_values: List[int], first_throw: bool = False
    ) -> int:
        """
        Calculates the score for a category without modifying the scoreboard.

        Args:
            category: The category to score.
            dice_values: The dice values to score.
            first_throw: Whether this was achieved on the first roll.

        Returns:
            The calculated score for this category.

        Raises:
            ValueError: If category is invalid.
        """
        if category in Scoreboard.STAGE_1:
            return Scoreboard.score_stage_one(category, dice_values)
        elif category in Scoreboard.STAGE_2:
            return Scoreboard.score_stage_two(category, dice_values, first_throw)
        raise ValueError(f"Unknown category: {category}")

    @staticmethod
    def score_stage_one(category: Category, dice_values: List[int]) -> int:
        """
        Calculates score for stage one categories.

        Args:
            category: A stage one category.
            dice_values: The dice values to score.

        Returns:
            Score based on matching dice minus threshold.
        """
        counts = Counter(dice_values)
        target_map = {
            Category.ONES: DiceValue.ONE.value,
            Category.TWOS: DiceValue.TWO.value,
            Category.THREES: DiceValue.THREE.value,
            Category.FOURS: DiceValue.FOUR.value,
            Category.FIVES: DiceValue.FIVE.value,
            Category.SIXES: DiceValue.SIX.value,
        }
        target_value = target_map[category]
        return (
            counts.get(target_value, 0) - CombinationThreshold.THREE_OF_A_KIND.value
        ) * target_value

    @staticmethod
    def score_stage_two(
        category: Category, dice_values: List[int], first_throw: bool = False
    ) -> int:
        """
        Calculates score for stage two categories.

        Args:
            category: A stage two category.
            dice_values: The dice values to score.
            first_throw: Whether this was achieved on the first roll.

        Returns:
            Score with applicable bonuses and multipliers.
        """
        counts = Counter(dice_values)
        total_sum = sum(dice_values)
        score = 0
        combination_met = False

        if category == Category.PAIR:
            if any(v >= CombinationThreshold.PAIR.value for v in counts.values()):
                score = total_sum
                combination_met = True
        elif category == Category.TWO_PAIRS:
            if (
                list(counts.values()).count(CombinationThreshold.PAIR.value)
                >= CombinationThreshold.PAIR.value
                or CombinationThreshold.FOUR_OF_A_KIND.value in counts.values()
                or CombinationThreshold.POKER.value in counts.values()
            ):
                score = total_sum
                combination_met = True
        elif category == Category.THREE_OF_A_KIND:
            if any(
                v >= CombinationThreshold.THREE_OF_A_KIND.value for v in counts.values()
            ):
                score = total_sum
                combination_met = True
        elif category == Category.FOUR_OF_A_KIND:
            if any(
                v >= CombinationThreshold.FOUR_OF_A_KIND.value for v in counts.values()
            ):
                score = total_sum
                combination_met = True
        elif category == Category.SMALL_STRAIGHT:
            unique_dice = frozenset(dice_values)
            if any(s.value.issubset(unique_dice) for s in SmallStraight):
                score = total_sum
                combination_met = True
        elif category == Category.LARGE_STRAIGHT:
            unique_dice = frozenset(dice_values)
            if any(unique_dice == s.value for s in LargeStraight):
                score = total_sum
                combination_met = True
        elif category == Category.EVEN:
            if all(d % CombinationThreshold.PAIR.value == 0 for d in dice_values):
                score = total_sum
                combination_met = True
        elif category == Category.ODD:
            if all(d % CombinationThreshold.PAIR.value != 0 for d in dice_values):
                score = total_sum
                combination_met = True
        elif category == Category.FULL_HOUSE:
            if (
                CombinationThreshold.FULL_HOUSE_THREE.value in counts.values()
                and CombinationThreshold.FULL_HOUSE_TWO.value in counts.values()
            ):
                score = total_sum
                combination_met = True
        elif category == Category.POKER:
            if CombinationThreshold.POKER.value in counts.values():
                score = total_sum + Bonus.POKER_BONUS.value
                combination_met = True
        elif category == Category.CHANCE:
            score = total_sum
            combination_met = True

        if not combination_met:
            return 0
        if first_throw and category != Category.CHANCE:
            if category == Category.POKER:
                return (
                    total_sum * Bonus.FIRST_THROW_MULTIPLIER.value
                ) + Bonus.POKER_BONUS.value
            return score * Bonus.FIRST_THROW_MULTIPLIER.value
        return score

    def __str__(self) -> str:
        """Returns a formatted string representation of the scoreboard."""
        lines = ["--- STAGE 1 ---"]
        for cat in self.STAGE_1:
            val = self.scores[cat]
            lines.append(f"{cat.value:16}: {val if val is not None else '-'}")
        lines.append(f"SUBTOTAL (S1): {self.get_stage_one_subtotal()}")
        if self.get_stage_one_subtotal() >= 0:
            lines.append(f"BONUS:           {Bonus.STAGE_ONE_BONUS.value}")
        lines.append("\n--- STAGE 2 ---")
        for cat in self.STAGE_2:
            val = self.scores[cat]
            lines.append(f"{cat.value:16}: {val if val is not None else '-'}")
        lines.append("--------------------")
        lines.append(f"TOTAL: {self.get_total_score()}")
        return "\n".join(lines)
