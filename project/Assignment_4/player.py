import random
from typing import List
from collections import Counter
from .scoreboard import Scoreboard, Category, DiceValue, CombinationThreshold


class Player:
    """Base class for all player types in the Yahtzee game."""

    def __init__(self, name: str) -> None:
        """
        Initializes a player with a name and empty scoreboard.
        Args:
            name: The player's name.
        """
        self.name: str = name
        self.scoreboard: Scoreboard = Scoreboard()

    def get_total_score(self) -> int:
        """Returns the player's total score from their scoreboard."""
        return self.scoreboard.get_total_score()

    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        """
        Decides which category to aim for based on current dice.
        Args:
            dice_values: Current values of all dice.
        Returns:
            The target category for this turn.
        """
        raise NotImplementedError("This method must be implemented by subclass.")

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        """
        Decides which dice to reroll based on the goal category.
        Args:
            dice_values: Current values of all dice.
            goal_category: The category being targeted.
        Returns:
            List of indices of dice to reroll.
        """
        raise NotImplementedError("This method must be implemented by subclass.")

    def _standard_reroll_logic(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        """
        Standard reroll logic that keeps dice matching the target value.
        Args:
            dice_values: Current values of all dice.
            goal_category: The category being targeted.
        Returns:
            List of indices of dice to reroll.
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
        """Returns a string representation of the player."""
        return f"{self.__class__.__name__}(name={self.name}, score={self.get_total_score()})"


class AggressiveBot(Player):
    """Bot that selects the category with the maximum potential score."""

    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        """
        Chooses the available category with the highest potential score.
        Args:
            dice_values: Current values of all dice.
        Returns:
            The category with maximum potential score.
        """
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
        """Uses standard reroll logic to maximize goal category score."""
        return self._standard_reroll_logic(dice_values, goal_category)


class CautiousBot(Player):
    """Bot that prioritizes safe scoring options and stage one categories."""

    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        """
        Chooses categories conservatively, favoring safe scoring options.
        Args:
            dice_values: Current values of all dice.
        Returns:
            A safe category to target.
        """
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
        """Uses standard reroll logic for conservative play."""
        return self._standard_reroll_logic(dice_values, goal_category)


class RandomBot(Player):
    """Bot that makes completely random decisions."""

    def decide_turn_goal(self, dice_values: List[int]) -> Category:
        """
        Randomly selects an available category.
        Args:
            dice_values: Current values of all dice (ignored).
        Returns:
            A randomly chosen category.
        """
        available = self.scoreboard.get_available_categories()
        return random.choice(available)

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: Category
    ) -> List[int]:
        """
        Randomly decides which dice to reroll.
        Args:
            dice_values: Current values of all dice.
            goal_category: The category being targeted (ignored).
        Returns:
            A random list of dice indices to reroll.
        """
        num_to_reroll = random.randint(0, len(dice_values))
        indices = list(range(len(dice_values)))
        return random.sample(indices, num_to_reroll)
