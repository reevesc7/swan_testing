from typing import Sequence
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(slots=True, kw_only=True)
class CurrentGenerator(ABC):
    @abstractmethod
    def update(self, dt: float, v: float) -> float: ...

    @abstractmethod
    def input_pulses(self, pulse_vals: Sequence[float]) -> None: ...

