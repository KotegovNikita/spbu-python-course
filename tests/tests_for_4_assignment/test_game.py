# tests/tests_for_4_assignment/test_game.py
import pytest
from project.Assignment_4.scoreboard import Scoreboard
from project.Assignment_4.player import Player, AggressiveBot, CautiousBot
from project.Assignment_4.Game import GameState, YahtzeeGame


def test_score_stage_one():
    """Tests the scoring logic for the upper section."""
    assert Scoreboard.score_stage_one("threes", [3, 3, 3, 3, 1]) == 3
    # ИСПРАВЛЕНО: Правильный результат (2-3)*4 = -4
    assert Scoreboard.score_stage_one("fours", [4, 4, 1, 2, 5]) == -4
    assert Scoreboard.score_stage_one("sixes", [6, 6, 6, 1, 2]) == 0
    assert Scoreboard.score_stage_one("ones", [2, 3, 4, 5, 6]) == -3


def test_score_stage_two():
    """Tests the scoring logic for the lower section."""
    assert Scoreboard.score_stage_two("poker", [5, 5, 5, 5, 5]) == 5 * 5 + 50
    assert Scoreboard.score_stage_two("full_house", [2, 2, 3, 3, 3]) == 13
    assert Scoreboard.score_stage_two("large_straight", [1, 2, 3, 4, 5]) == 15
    # ИСПРАВЛЕНО: Правильный результат - сумма всех костей (1+1+2+3+4 = 11)
    assert Scoreboard.score_stage_two("pair", [1, 1, 2, 3, 4]) == 11
    assert Scoreboard.score_stage_two("four_of_a_kind", [1, 2, 3, 4, 5]) == 0
    assert Scoreboard.score_stage_two("poker", [1, 1, 1, 1, 2]) == 0


def test_stage_one_bonus():
    """Tests the +50 bonus for the upper section."""
    sb = Scoreboard()
    sb.scores["ones"] = 0
    sb.scores["twos"] = 0
    sb.scores["threes"] = 0
    sb.scores["fours"] = -4
    sb.scores["fives"] = 5
    sb.scores["sixes"] = 0
    assert sb.get_stage_one_subtotal() == 1
    assert sb.get_total_score() == 51

    sb.scores["fours"] = -8
    assert sb.get_stage_one_subtotal() == -3
    assert sb.get_total_score() == -3


def test_fill_category_twice_raises_error():
    """Tests that filling an already filled category raises a ValueError."""
    sb = Scoreboard()
    sb.fill_category("ones", [1, 1, 1, 2, 3])
    with pytest.raises(ValueError):
        sb.fill_category("ones", [1, 1, 1, 1, 1])


def test_game_state_advancement():
    """Tests the advancement of game state (players and rounds)."""
    p1 = AggressiveBot("P1")
    p2 = CautiousBot("P2")
    state = GameState([p1, p2])

    assert state.current_round == 0
    assert state.get_current_player() == p1

    state.advance_turn()
    assert state.current_round == 0
    assert state.get_current_player() == p2

    state.advance_turn()
    assert state.current_round == 1
    assert state.get_current_player() == p1


def test_game_over_condition():
    """Tests that the game correctly identifies when it is over."""
    p1 = AggressiveBot("P1")
    state = GameState([p1])
    assert not state.is_game_over()

    # ИСПРАВЛЕНО: Цикл теперь выполняется столько раз, сколько раундов в игре
    for _ in range(state.max_rounds):
        state.advance_turn()

    assert state.is_game_over()


def test_winner_determination():
    """Tests the winner determination logic, including ties."""
    p1 = AggressiveBot("P1")
    p2 = CautiousBot("P2")
    p3 = CautiousBot("P3")

    p1.scoreboard.scores["chance"] = 30
    p2.scoreboard.scores["chance"] = 20
    p3.scoreboard.scores["chance"] = 30

    game = YahtzeeGame([p1, p2, p3], verbose=False)
    game._determine_winner()

    assert game.winner is None

    p1.scoreboard.scores["poker"] = 50
    game._determine_winner()
    assert game.winner == p1
