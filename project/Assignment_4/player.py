# player.py
import random
from typing import List
from collections import Counter
from .scoreboard import Scoreboard


class Player:
    def __init__(self, name: str):
        """
        Initializes the player.

        Args:
            name : The player's name.
        """
        self.name = name
        self.scoreboard = Scoreboard()

    def get_total_score(self) -> int:
        """
        Returns the player's current total score.

        Returns:
            int: The total score.
        """
        return self.scoreboard.get_total_score()

    def decide_turn_goal(self, dice_values: List[int]) -> str:
        """
        Analyzes the first roll and decides which category to play for this turn.

        Args:
            dice_values : The dice values after the first roll.

        Returns:
            str: The name of the target category.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: str
    ) -> List[int]:
        """
        Based on the turn's goal, decides which dice to reroll.

        Args:
            dice_values : The current dice values.
            goal_category : The target category for this turn.

        Returns:
            List[int]: A list of dice indices to reroll.
        """
        raise NotImplementedError("This method should be implemented by a subclass.")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, score={self.get_total_score()})"


class AggressiveBot(Player):
    def decide_turn_goal(self, dice_values: List[int]) -> str:
        available = self.scoreboard.get_available_categories()
        best_category = ""
        max_potential_score = -100

        for category in available:
            potential_score = Scoreboard.score_for_category(category, dice_values)
            if potential_score > max_potential_score:
                max_potential_score = potential_score
                best_category = category

        return best_category if best_category else available[0]

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: str
    ) -> List[int]:
        counts = Counter(dice_values)
        target_map = {
            "ones": 1,
            "twos": 2,
            "threes": 3,
            "fours": 4,
            "fives": 5,
            "sixes": 6,
        }

        if goal_category in target_map:
            target_value = target_map[goal_category]
            return [i for i, v in enumerate(dice_values) if v != target_value]

        if goal_category in [
            "pair",
            "two_pairs",
            "three_of_a_kind",
            "four_of_a_kind",
            "full_house",
            "poker",
            "chance",
        ]:
            if not dice_values:
                return []
            target_value = counts.most_common(1)[0][0]
            return [i for i, v in enumerate(dice_values) if v != target_value]

        return []


class CautiousBot(Player):
    def decide_turn_goal(self, dice_values: List[int]) -> str:
        available = self.scoreboard.get_available_categories()
        counts = Counter(dice_values)

        value_map = {
            1: "ones",
            2: "twos",
            3: "threes",
            4: "fours",
            5: "fives",
            6: "sixes",
        }
        for value, count in counts.most_common():
            if count >= 2:
                category = value_map[value]
                if category in available:
                    return category

        for cat in Scoreboard.stage_1_st:
            if cat in available:
                return cat

        if "chance" in available:
            return "chance"
        return available[0]

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: str
    ) -> List[int]:
        return AggressiveBot.make_reroll_decision(self, dice_values, goal_category)


class RandomBot(Player):
    def decide_turn_goal(self, dice_values: List[int]) -> str:
        available = self.scoreboard.get_available_categories()
        return random.choice(available)

    def make_reroll_decision(
        self, dice_values: List[int], goal_category: str
    ) -> List[int]:
        num_to_reroll = random.randint(0, len(dice_values))
        indices = list(range(len(dice_values)))
        return random.sample(indices, num_to_reroll)
