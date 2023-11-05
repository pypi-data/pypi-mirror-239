from ...alpha_classes import AlphaGameResult
from ...expansion_login.mcts_search.Node import Node


def backpropagate(node: Node, results: dict[int, AlphaGameResult]) -> None:
    while node is not None:
        node.visits += 1
        node.value += results[node.state.current_player.id].value
        node = node.parent
