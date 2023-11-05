from typing import Optional, Self

from ...alpha_classes import AlphaTrainableGame


class Node:
    def __init__(self, state: AlphaTrainableGame, parent: Optional[Self] = None):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(list(self.state.get_possible_actions()))
