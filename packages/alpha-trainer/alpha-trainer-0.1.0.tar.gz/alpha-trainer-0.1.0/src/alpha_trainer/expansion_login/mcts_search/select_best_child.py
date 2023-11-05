from .Node import Node


def select_best_child(node: Node) -> Node:
    best_child = None
    best_value = -float("inf")
    for child in node.children.values():
        child_value = child.value / child.visits
        if child_value > best_value:
            best_value = child_value
            best_child = child
    return best_child
