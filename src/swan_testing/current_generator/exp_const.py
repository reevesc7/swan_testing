from typing import Sequence
from dataclasses import dataclass
from math import exp, log
from .current_generator import CurrentGenerator


@dataclass(slots=True)
class ExpConstCurrent(CurrentGenerator):
    ninety_pct_time: float
    k: float
    current: float
    target_current: float

    def __init__(self, ninety_pct_time: float) -> None:
        self.ninety_pct_time = ninety_pct_time
        self.k = log(0.1) / ninety_pct_time
        self.current = 0.0
        self.target_current = 0.0

    def alpha(self, dt: float) -> float:
        return 1 - exp(self.k * dt)

    def update(self, dt: float) -> float:
        self.current += self.alpha(dt) * (self.target_current - self.current)
        return self.current

    def input_pulses(self, pulse_vals: Sequence[float]) -> None:
        self.target_current = sum(pulse_vals)

