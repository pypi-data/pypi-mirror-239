from abc import abstractmethod, ABC
from typing import Sequence, TYPE_CHECKING, Self

from .AlphaGameResult import AlphaGameResult

from .AlphaPlayer import AlphaPlayer

if TYPE_CHECKING:
    from ..alpha_classes import AlphaMove


AlphaGameResults = dict[int, AlphaGameResult]


class AlphaTrainableGame(ABC):
    players: list
    current_player: AlphaPlayer
    players: Sequence[AlphaPlayer]

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def copy(self) -> Self:
        pass

    @abstractmethod
    def perform(self, action: "AlphaMove") -> Self:
        pass

    @abstractmethod
    def get_possible_actions(self) -> list["AlphaMove"]:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass

    @abstractmethod
    def get_results(self) -> AlphaGameResults:
        pass

    @abstractmethod
    def get_state(self) -> tuple:
        pass
