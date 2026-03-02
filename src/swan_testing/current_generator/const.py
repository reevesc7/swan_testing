from typing import Sequence
from dataclasses import dataclass
from .current_generator import CurrentGenerator


@dataclass(slots=True)
class ConstCurrent(CurrentGenerator):
    current: float = 0.0

    def update(self, dt: float) -> float:
        _ = dt
        return self.current

    def input_pulses(self, pulse_vals: Sequence[float]) -> None:
        self.current = sum(pulse_vals)

