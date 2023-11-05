import math

from .Node import Node
from .expand import expand


def select_child(node: Node) -> Node:
    possible_actions = list(node.state.get_possible_actions())
    if not node.is_fully_expanded():
        return expand(node)
    else:
        best_child = None
        best_uct = -float("inf")
        for action in possible_actions:
            child = node.children[action]
            uct = (child.value / (child.visits + 1)) + (
                math.sqrt(2 * math.log(node.visits) / (child.visits + 1))
            )
            if uct > best_uct:
                best_uct = uct
                best_child = child
        return best_child
