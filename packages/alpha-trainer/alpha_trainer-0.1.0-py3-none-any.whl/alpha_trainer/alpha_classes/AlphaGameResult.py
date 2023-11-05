from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class AlphaGameResult(ABC):
    value: float

    def __post_init__(self):
        if not -1 <= self.value <= 1:
            raise ValueError("Result must be in -1, 1 range")
