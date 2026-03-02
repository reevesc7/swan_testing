from typing import Sequence
from dataclasses import dataclass
from .current_generator import CurrentGenerator


@dataclass(slots=True)
class NullCurrent(CurrentGenerator):
    def update(self, dt: float) -> float:
        _ = dt
        return 0.0

    def input_pulses(self, pulse_vals: Sequence[float]) -> None:
        _ = pulse_vals
        pass


