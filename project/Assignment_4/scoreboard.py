from typing import List, Dict, Set
from collections import Counter


class Scoreboard:
    stage_1_st = ["ones", "twos", "threes", "fours", "fives", "sixes"]
    stage_2_nd = [
        "pair",
        "two_pairs",
        "three_of_a_kind",
        "four_of_a_kind",
        "small_straight",
        "large_straight",
        "even",
        "odd",
        "full_house",
        "poker",
        "chance",
    ]
    CATEGORIES = stage_1_st + stage_2_nd

    def __init__(self):
        self.scores: Dict[str, int | None] = {c: None for c in self.CATEGORIES}

    def get_available_categories(self) -> List[str]:
        """
        Returns a list of categories that have not yet been filled.

        Returns:
            List[str]: A list of names of available categories.
        """
        return [c for c, v in self.scores.items() if v is None]

    def get_stage_one_subtotal(self) -> int:
        """
        Calculates the subtotal for the first stage (from 'ones' to 'sixes').

        Returns:
            int: The sum of scores for the first stage.
        """
        return sum(
            v for c, v in self.scores.items() if c in self.stage_1_st and v is not None
        )

    def is_complete(self) -> bool:
        """
        Checks if all categories on the scoreboard have been filled.

        Returns:
            bool: True if all categories are filled, otherwise False.
        """
        return all(v is not None for v in self.scores.values())

    def get_total_score(self) -> int:
        """
        Calculates the final total score, including the bonus for the first stage.

        Returns:
            int: The total score.
        """
        stage_one_total = self.get_stage_one_subtotal()
        stage_two_total = sum(
            v for c, v in self.scores.items() if c in self.stage_2_nd and v is not None
        )
        bonus = 50 if stage_one_total >= 0 else 0
        return stage_one_total + stage_two_total + bonus

    def fill_category(
        self, category: str, dice_values: List[int], first_throw: bool = False
    ) -> int:
        """
        Fills a category with a score calculated from the dice values.

        Args:
            category (str): The name of the category to fill.
            dice_values (List[int]): A list of the dice values.
            first_throw (bool): True if the combination was achieved on the first roll.

        Returns:
            int: The number of points scored.
        """
        if category not in self.CATEGORIES:
            raise ValueError(f"Unknown category: {category}")
        if self.scores[category] is not None:
            raise ValueError(f"Category '{category}' is already filled")
        score = Scoreboard.score_for_category(category, dice_values, first_throw)
        self.scores[category] = score
        return score

    @staticmethod
    def score_for_category(
        category: str, dice_values: List[int], first_throw: bool = False
    ) -> int:
        """
        Calculates the score for a given category without saving the result.

        Args:
            category (str): The name of the category.
            dice_values (List[int]): A list of the dice values.
            first_throw (bool): True if the combination was achieved on the first roll.

        Returns:
            int: The potential score.
        """
        if category in Scoreboard.stage_1_st:
            return Scoreboard.score_stage_one(category, dice_values)
        elif category in Scoreboard.stage_2_nd:
            return Scoreboard.score_stage_two(category, dice_values, first_throw)
        raise ValueError(f"Unknown category for scoring: {category}")

    @staticmethod
    def score_stage_one(category: str, dice_values: List[int]) -> int:
        """
        Calculates the score for the first stage categories.

        Args:
            category (str): The name of the category ('ones', 'twos', etc.).
            dice_values (List[int]): A list of the dice values.

        Returns:
            int: The score calculated by the formula (count - 3) * value.
        """
        counts = Counter(dice_values)
        target_map = {
            "ones": 1,
            "twos": 2,
            "threes": 3,
            "fours": 4,
            "fives": 5,
            "sixes": 6,
        }
        target_value = target_map[category]
        return (counts.get(target_value, 0) - 3) * target_value

    @staticmethod
    def score_stage_two(
        category: str, dice_values: List[int], first_throw: bool = False
    ) -> int:
        """
        Calculates the score for the second stage categories.

        Args:
            category (str): The name of the combination.
            dice_values (List[int]): A list of the dice values.
            first_throw (bool): True if the combination was achieved on the first roll.

        Returns:
            int: The score for the combination.
        """
        counts = Counter(dice_values)
        total_sum = sum(dice_values)
        score = 0
        combination_met = False

        if category == "pair":
            if any(v >= 2 for v in counts.values()):
                score = total_sum
                combination_met = True
        elif category == "two_pairs":
            if (
                list(counts.values()).count(2) >= 2
                or 4 in counts.values()
                or 5 in counts.values()
            ):
                score = total_sum
                combination_met = True
        elif category == "three_of_a_kind":
            if any(v >= 3 for v in counts.values()):
                score = total_sum
                combination_met = True
        elif category == "four_of_a_kind":
            if any(v >= 4 for v in counts.values()):
                score = total_sum
                combination_met = True
        elif category == "small_straight":
            unique_dice = set(dice_values)
            if any(
                s.issubset(unique_dice)
                for s in [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
            ):
                score = total_sum
                combination_met = True
        elif category == "large_straight":
            # Fixed: Removed re-definition with type hint to satisfy mypy
            unique_dice_large = set(dice_values)
            if unique_dice_large in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
                score = total_sum
                combination_met = True
        elif category == "even":
            if all(d % 2 == 0 for d in dice_values):
                score = total_sum
                combination_met = True
        elif category == "odd":
            if all(d % 2 != 0 for d in dice_values):
                score = total_sum
                combination_met = True
        elif category == "full_house":
            if 3 in counts.values() and 2 in counts.values():
                score = total_sum
                combination_met = True
        elif category == "poker":
            if 5 in counts.values():
                score = total_sum + 50
                combination_met = True
        elif category == "chance":
            score = total_sum
            combination_met = True

        if not combination_met:
            return 0
        if first_throw and category != "chance":
            if category == "poker":
                return (total_sum * 2) + 50
            return score * 2
        return score

    def __str__(self) -> str:
        lines = ["--- STAGE 1 ---"]
        for cat in self.stage_1_st:
            val = self.scores[cat]
            lines.append(f"{cat:16}: {val if val is not None else '-'}")
        lines.append(f"SUBTOTAL (S1): {self.get_stage_one_subtotal()}")
        if self.get_stage_one_subtotal() >= 0:
            lines.append("BONUS:           50")
        lines.append("\n--- STAGE 2 ---")
        for cat in self.stage_2_nd:
            val = self.scores[cat]
            lines.append(f"{cat:16}: {val if val is not None else '-'}")
        lines.append("--------------------")
        lines.append(f"TOTAL: {self.get_total_score()}")
        return "\n".join(lines)
