from typing import Iterable, Sequence, SupportsIndex
from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class Soma(ABC):
    spike_magnitude: float

    @abstractmethod
    def update(self, pulses: Sequence[float]) -> float: ...

    def pulses_train(self, pulses_vals: Iterable[Sequence[float]]) -> None:
        """Run the FHN for a set of updates with pulses given at each segment.
        #
        Parameters
        ----------
        `pulses_vals` : `Iterable[Sequence[float]]`
            The magnitudes of each pulse.
        """
        for pulses in pulses_vals:
            self.update(pulses)

    def pulses(self, pulses: Sequence[float], n_pulses: SupportsIndex) -> None:
        """Run the FHN for a set number of updates with pulses given at each segment.
        #
        Parameters
        ----------
        `pulses` : `Sequence[float]`
            The magnitudes of the each pulse.
        `n_pulses` : `SupportsIndex`
            The number of pulses to deliver.
        """
        for _ in range(n_pulses):
            self.update(pulses)

    def pulses_segments(self, pulses_vals: Iterable[tuple[Sequence[float], SupportsIndex]]) -> None:
        """Run the FHN for a set number of updates with pulses given at each segment.
        #
        Parameters
        ----------
        `magnitude` : `Sequence[float]`
            The magnitudes of the each pulse.
        `n_pulses` : `SupportsIndex`
            The number of pulses to deliver.
        """
        for pulses in pulses_vals:
            self.pulses(*pulses)

    @abstractmethod
    def history(self) -> pd.DataFrame: ...

