import pytest
from project.Assignment_4.dice import Dice
from project.Assignment_4.player import AggressiveBot, CautiousBot
from project.Assignment_4.scoreboard import Scoreboard, Category
from project.Assignment_4.Game import Turn, GameState, YahtzeeGame


class TestDice:
    def test_dice_changes(self):
        dice = Dice()
        original = dice.value
        for _ in range(10):
            dice.roll()
            if dice.value != original:
                break
        assert 1 <= dice.value <= 6


class TestScoreboard:
    def test_fill_category(self):
        sb = Scoreboard()
        initial = len(sb.get_available_categories())
        sb.fill_category(Category.ONES, [1, 1, 1, 2, 3])
        assert len(sb.get_available_categories()) == initial - 1

    def test_cannot_twice(self):
        sb = Scoreboard()
        sb.fill_category(Category.ONES, [1, 1, 1, 2, 3])
        with pytest.raises(ValueError):
            sb.fill_category(Category.ONES, [1, 1, 1, 1, 1])

    def test_bonus(self):
        sb = Scoreboard()
        score = sb.fill_category(Category.POKER, [6, 6, 6, 6, 6])
        assert score == 80


class TestTurn:
    def test_roll_count(self):
        player = AggressiveBot("Bot")
        turn = Turn(player)
        turn.roll_dice()
        assert turn.roll_count == 1

    def test_three_rolls(self):
        player = AggressiveBot("Bot")
        turn = Turn(player)
        turn.roll_dice()
        turn.roll_dice()
        turn.roll_dice()
        with pytest.raises(ValueError):
            turn.roll_dice()


class TestGameState:
    def test_advance_player(self):
        players = [AggressiveBot("Bot1"), CautiousBot("Bot2")]
        state = GameState(players)
        assert state.get_current_player().name == "Bot1"
        state.advance_turn()
        assert state.get_current_player().name == "Bot2"

    def test_round(self):
        players = [AggressiveBot("Bot1"), CautiousBot("Bot2")]
        state = GameState(players)
        state.advance_turn()
        state.advance_turn()
        assert state.current_round == 1


class TestYahtzeeGame:
    def test_full_game(self):
        players = [AggressiveBot("Bot1"), CautiousBot("Bot2")]
        game = YahtzeeGame(players, verbose=False)
        game.play_game()

        assert game.state.is_game_over()
        for player in players:
            assert player.scoreboard.is_complete()
