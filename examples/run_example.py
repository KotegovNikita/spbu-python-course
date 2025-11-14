import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project.Assignment_4.player import AggressiveBot, CautiousBot, RandomBot
from project.Assignment_4.Game import YahtzeeGame


def run_simulation():
    print("Initializing a new game of Yahtzee with three distinct bot strategies...")

    players = [
        AggressiveBot("AggroBot"),
        CautiousBot("CautiousBot"),
        RandomBot("RandomBot"),
    ]

    game = YahtzeeGame(players=players, verbose=True)
    game.play_game()


if __name__ == "__main__":
    run_simulation()
