import random
from typing import List
from collections import Counter
from .scoreboard import Scoreboard, Category, DiceValue, CombinationThreshold


class Player:
    def __init__(self, name: str):
        self.name = name
        self.scoreboard = Scoreboard()

    def get_total_score(self) -> int:
        return self.scoreboard.get_total_score()

    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        raise NotImplementedError("Этот метод должен быть реализован подклассом.")

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        raise NotImplementedError("Этот метод должен быть реализован подклассом.")

    def _standard_reroll_logic(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        """Стандартная логика переброски: оставляет кубики, соответствующие цели"""
        counts = Counter(dice_values)
        target_map = {
            Category.ONES: DiceValue.ONE.value,
            Category.TWOS: DiceValue.TWO.value,
            Category.THREES: DiceValue.THREE.value,
            Category.FOURS: DiceValue.FOUR.value,
            Category.FIVES: DiceValue.FIVE.value,
            Category.SIXES: DiceValue.SIX.value,
        }

        if goal_category in target_map:
            target_value = target_map[goal_category]
            return [i for i, v in enumerate(dice_values) if v != target_value]

        if goal_category in [
            Category.PAIR,
            Category.TWO_PAIRS,
            Category.THREE_OF_A_KIND,
            Category.FOUR_OF_A_KIND,
            Category.FULL_HOUSE,
            Category.POKER,
            Category.CHANCE,
        ]:
            if not dice_values:
                return []
            target_value = counts.most_common(1)[0][0]
            return [i for i, v in enumerate(dice_values) if v != target_value]

        return []

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, score={self.get_total_score()})"


class AggressiveBot(Player):
    """Бот, выбирающий категорию с максимальным потенциальным счетом"""

    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        available = self.scoreboard.get_available_categories()
        best_category = None
        max_potential_score = float("-inf")

        for category in available:
            potential_score = Scoreboard.score_for_category(category, dice_values)
            if potential_score > max_potential_score:
                max_potential_score = potential_score
                best_category = category

        return best_category if best_category else available[0]

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        return self._standard_reroll_logic(dice_values, goal_category)


class CautiousBot(Player):
    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        available = self.scoreboard.get_available_categories()
        counts = Counter(dice_values)

        value_map = {
            DiceValue.ONE.value: Category.ONES,
            DiceValue.TWO.value: Category.TWOS,
            DiceValue.THREE.value: Category.THREES,
            DiceValue.FOUR.value: Category.FOURS,
            DiceValue.FIVE.value: Category.FIVES,
            DiceValue.SIX.value: Category.SIXES,
        }

        for value, count in counts.most_common():
            if count >= CombinationThreshold.PAIR.value:
                category = value_map[value]
                if category in available:
                    return category

        for cat in Scoreboard.STAGE_1:
            if cat in available:
                return cat

        if Category.CHANCE in available:
            return Category.CHANCE
        return available[0]

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        return self._standard_reroll_logic(dice_values, goal_category)


class RandomBot(Player):
    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        available = self.scoreboard.get_available_categories()
        return random.choice(available)

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        num_to_reroll = random.randint(0, len(dice_values))
        indices = list(range(len(dice_values)))
        return random.sample(indices, num_to_reroll)
