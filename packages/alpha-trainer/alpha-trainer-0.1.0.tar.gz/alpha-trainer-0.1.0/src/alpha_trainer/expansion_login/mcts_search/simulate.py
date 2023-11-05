import random

from ...alpha_classes import AlphaMove
from ...alpha_classes import (
    AlphaTrainableGame,
)
from ...alpha_classes import AlphaGameResults


def simulate(state: AlphaTrainableGame) -> AlphaGameResults:
    while not state.is_terminal():
        possible_actions = state.get_possible_actions()
        action: AlphaMove = random.choice(possible_actions)
        state.perform(action)
    return state.get_results()
