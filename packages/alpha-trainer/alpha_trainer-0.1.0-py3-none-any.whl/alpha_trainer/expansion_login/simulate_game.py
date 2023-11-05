from typing import Type, Callable
from .mcts_search import mcts_search
from .model_prediction import model_prediction
from .. import AlphaTrainableGame, AlphaMove

StatesAndResults = dict[tuple, float]


def simulate_game(
    game_class: Type[AlphaTrainableGame],
    num_simulations: int = None,
    model=None,
    game_args: tuple = None,
    game_kwargs: dict = None,
    choice_function: Callable[[dict[AlphaMove, float]], AlphaMove] = None,
) -> StatesAndResults:
    if not issubclass(game_class, AlphaTrainableGame):
        raise ValueError(f"Game class must be a subclass of AlphaTrainableGame")
    if num_simulations is None and model is None:
        raise ValueError("Either model or number_of_simulations must be provided")
    states = {}
    root = game_class(*(game_args or ()), **(game_kwargs or {}))
    states[root.get_state()] = root.current_player.id
    while not root.is_terminal():
        current_player_id = root.current_player.id
        root = (
            model_prediction(root, model, choice_function)
            if model
            else mcts_search(root, num_simulations)
        )
        states[root.get_state()] = current_player_id
    return score_positions(root, states)


def score_positions(
    game: AlphaTrainableGame, states: dict[tuple, int]
) -> StatesAndResults:
    results = game.get_results()
    return dict(
        (state, results[player_id].value) for state, player_id in states.items()
    )
