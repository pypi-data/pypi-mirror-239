from ...alpha_classes import (
    AlphaTrainableGame,
)
from .Node import Node
from .backpropagate import backpropagate
from .expand import expand
from .select_best_child import select_best_child
from .select_child import select_child
from .simulate import simulate


def mcts_search(
    root_state: AlphaTrainableGame, num_simulations: int
) -> AlphaTrainableGame:
    root_node = Node(root_state)

    for _ in range(num_simulations):
        node = root_node

        # Selection
        while not node.state.is_terminal() and node.is_fully_expanded():
            node = select_child(node)

        # Expansion
        if not node.state.is_terminal() and not node.is_fully_expanded():
            node = expand(node)

        # Simulation
        result = simulate(node.state.copy())

        # Backpropagation
        backpropagate(node, result)

    best_child = select_best_child(root_node)
    return best_child.state
