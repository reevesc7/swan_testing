from typing import Sequence
from dataclasses import dataclass
from .current_generator import CurrentGenerator


@dataclass(slots=True)
class SmoothConstCurrent(CurrentGenerator):
    smooth_time: float
    current: float = 0.0
    last_current: float = 0.0
    time_since_current_change: float = 0.0

    @staticmethod
    def smoothstep(t: float) -> float:
        if t > 1.0:
            return 1.0
        return 3 * t ** 2 - 2 * t ** 3

    def update(self, dt: float) -> float:
        smooth_coeff = self.smoothstep(self.time_since_current_change / self.smooth_time)
        current_diff = self.current - self.last_current
        self.time_since_current_change += dt
        return self.last_current + smooth_coeff * current_diff

    def input_pulses(self, pulse_vals: Sequence[float]) -> None:
        self.last_current = self.current
        self.current = sum(pulse_vals)
        self.time_since_current_change = 0.0

