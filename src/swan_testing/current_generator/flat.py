from typing import Sequence
from dataclasses import dataclass, field
from .current_generator import CurrentGenerator


@dataclass(slots=True)
class FlatCurrent_:
    time: float
    i: float

    def update(self, dt: float) -> float:
        if round(self.time, 4) > 0.0:
            self.time -= dt
            return self.i
        return 0.0

    def is_active(self) -> bool:
        return round(self.time, 4) > 0.0


@dataclass(slots=True)
class FlatCurrent(CurrentGenerator):
    current_duration: float
    currents: list[FlatCurrent_] = field(default_factory=list)

    def update(self, dt: float) -> float:
        total_i = sum(current.update(dt) for current in self.currents)
        self.currents = [current for current in self.currents if current.is_active()]
        return total_i

    def input_pulses(self, pulse_vals: Sequence[float]) -> None:
        for pulse in pulse_vals:
            self.currents.append(FlatCurrent_(self.current_duration, pulse))

