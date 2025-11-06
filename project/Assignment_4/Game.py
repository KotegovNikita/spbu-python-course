from typing import List, Optional
from .dice import Dice
from .player import Player
from .scoreboard import Scoreboard, Category


class Turn:
    """Manages a single turn for a player in Yahtzee."""

    def __init__(self, player: Player, num_dice: int = 5) -> None:
        """
        Initializes a turn for the specified player.

        Args:
            player: The player taking the turn.
            num_dice: The number of dice in the game.
        """
        self.player: Player = player
        self.dice: List[Dice] = [Dice() for _ in range(num_dice)]
        self.roll_count: int = 0
        self.current_values: List[int] = []

    def roll_dice(self, indices_to_roll: Optional[List[int]] = None) -> List[int]:
        """
        Rolls the specified dice and updates their values.

        Args:
            indices_to_roll: A list of dice indices to roll. If None, rolls all dice.
        Returns:
            The new list of all dice values.
        Raises:
            ValueError: If maximum rolls (3) have been exceeded.
        """
        if self.roll_count >= 3:
            raise ValueError("Max rolls exceeded")
        if indices_to_roll is None:
            indices_to_roll = list(range(len(self.dice)))
        for i in indices_to_roll:
            if 0 <= i < len(self.dice):
                self.dice[i].roll()
        self.current_values = [d.value for d in self.dice]
        self.roll_count += 1
        return self.current_values

    def can_reroll(self) -> bool:
        """
        Checks if the player can make another roll this turn.

        Returns:
            True if the roll count is less than 3.
        """
        return self.roll_count < 3

    def get_dice_values(self) -> List[int]:
        """
        Returns the current values of the dice.

        Returns:
            A copy of the list of dice values.
        """
        return self.current_values.copy()

    def finalize(self, category: Category) -> int:
        """
        Ends the turn by scoring the result in the specified category.

        Args:
            category: The name of the category to fill.
        Returns:
            The number of points scored.
        Raises:
            ValueError: If no rolls have been made.
        """
        if self.roll_count == 0:
            raise ValueError("Must roll at least once")
        is_first_throw = self.roll_count == 1
        return self.player.scoreboard.fill_category(
            category, self.current_values, first_throw=is_first_throw
        )


class GameState:
    """Tracks the current state of the Yahtzee game."""

    def __init__(self, players: List[Player]) -> None:
        """
        Initializes the game state.

        Args:
            players: The list of players in the game.
        """
        self.players: List[Player] = players
        self.max_rounds: int = len(Scoreboard.CATEGORIES)
        self.current_round: int = 0
        self.current_player_index: int = 0

    def get_current_player(self) -> Player:
        """
        Returns the player whose turn it is.

        Returns:
            The current active player.
        """
        return self.players[self.current_player_index]

    def advance_turn(self) -> None:
        """Advances the turn to the next player and round if necessary."""
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
            self.current_round += 1

    def is_game_over(self) -> bool:
        """
        Checks if the game has ended.

        Returns:
            True if the number of rounds played has reached the maximum.
        """
        return self.current_round >= self.max_rounds

    def __str__(self) -> str:
        """Returns a string representation of the current game state."""
        leaderboard = sorted(
            self.players, key=lambda p: p.get_total_score(), reverse=True
        )
        lines = [
            f"\n{'=' * 20} ROUND {self.current_round + 1}/{self.max_rounds} {'=' * 20}",
            f"Current Player: {self.get_current_player().name}",
            "Leaderboard:",
        ]
        for p in leaderboard:
            lines.append(f"  - {p.name}: {p.get_total_score()} points")
        return "\n".join(lines)


class YahtzeeGame:
    """Manages the overall game flow, players, and rounds."""

    def __init__(self, players: List[Player], verbose: bool = True) -> None:
        """
        Initializes the Yahtzee game.

        Args:
            players: A list of players participating in the game.
            verbose: If True, prints the game log to the console.
        Raises:
            ValueError: If no players are provided.
        """
        if not players:
            raise ValueError("At least one player is required")
        self.state: GameState = GameState(players)
        self.verbose: bool = verbose
        self.winner: Optional[Player] = None

    def get_game_state(self) -> GameState:
        """
        Returns the current state of the game.

        Returns:
            The object holding the game's current state.
        """
        return self.state

    def play_turn(self, player: Player) -> None:
        """
        Conducts one full turn for a single player.

        Args:
            player: The player taking the turn.
        """
        turn = Turn(player)
        if self.verbose:
            print(f"\n--- {player.name}'s turn ---")

        dice = turn.roll_dice()
        goal_category = player.decide_turn_goal(dice)
        if self.verbose:
            print(f"Roll 1: {dice}")
            print(f"  -> Bot decided to go for category: '{goal_category}'")

        while turn.can_reroll():
            indices = player.make_reroll_decision(turn.get_dice_values(), goal_category)
            if not indices:
                if self.verbose:
                    print("  -> Bot keeps dice")
                break

            if self.verbose:
                print(f"  -> Bot rerolls indices: {[i + 1 for i in indices]}")
            dice = turn.roll_dice(indices)
            if self.verbose:
                print(f"Roll {turn.roll_count}: {dice}")

        points = turn.finalize(goal_category)
        if self.verbose:
            print(f"  -> Final dice: {turn.get_dice_values()}")
            print(f"  -> Result scored in '{goal_category}'. Points: {points}")
            print(f"  -> Player's total score: {player.get_total_score()}")

    def play_game(self) -> None:
        """Plays a complete game of Yahtzee from start to finish."""
        if self.verbose:
            print("\n" + "=" * 50 + "\nYAHTZEE GAME START\n" + "=" * 50)
            print(f"Players: {', '.join(str(p) for p in self.state.players)}")

        while not self.state.is_game_over():
            if self.verbose:
                print(self.state)
            player = self.state.get_current_player()
            self.play_turn(player)
            self.state.advance_turn()

        self._determine_winner()
        if self.verbose:
            self.print_final_results()

    def _determine_winner(self) -> None:
        """Determines the winner(s) at the end of the game."""
        if not self.state.players:
            return
        max_score = max(p.get_total_score() for p in self.state.players)
        winners = [p for p in self.state.players if p.get_total_score() == max_score]
        self.winner = winners[0] if len(winners) == 1 else None

    def print_final_results(self) -> None:
        """Prints the final game results and scoreboard."""
        print("\n" + "=" * 50 + "\nGAME OVER - FINAL RESULTS\n" + "=" * 50)
        leaderboard = sorted(
            self.state.players, key=lambda p: p.get_total_score(), reverse=True
        )

        all_scores = [p.get_total_score() for p in self.state.players]
        average_score = sum(all_scores) / len(all_scores) if all_scores else 0

        print(f"Average score for the game: {average_score:.2f}\n")

        for i, player in enumerate(leaderboard, 1):
            score = player.get_total_score()
            win_loss = score - average_score
            sign = "+" if win_loss >= 0 else ""
            print(
                f"{i}. {player.name} - {score} points (Win/Loss: {sign}{win_loss:.2f})"
            )
            print(player.scoreboard)

        if self.winner:
            print(f"\n WINNER: {self.winner.name}! ")
        else:
            top_score = leaderboard[0].get_total_score()
            winners = [p.name for p in leaderboard if p.get_total_score() == top_score]
            print(f"\n TIE between: {', '.join(winners)}")
