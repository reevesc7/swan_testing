from typing import Sequence
from dataclasses import dataclass
import pandas as pd
from .soma import Soma
from ..current_receiver.current_receiver import CurrentReceiver
from ..current_generator.current_generator import CurrentGenerator


@dataclass(slots=True)
class CurrentSoma(Soma):
    current_generator: CurrentGenerator
    current_receiver: CurrentReceiver
    dt: float
    time_per_update: float

    def update(self, pulses: Sequence[float]) -> float:
        self.current_generator.input_pulses(pulses)
        n_spikes = 0
        for _ in range(int(self.time_per_update / self.dt)):
            i = self.current_generator.update(self.dt)
            n_spikes += self.current_receiver.update(i, self.dt)
        return n_spikes * self.spike_magnitude

    def history(self) -> pd.DataFrame:
        return self.current_receiver.history()

