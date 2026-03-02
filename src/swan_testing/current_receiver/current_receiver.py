from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd


@dataclass(slots=True)
class CurrentReceiver(ABC):
    @abstractmethod
    def update(self, i: float, dt: float) -> bool: ...

    @abstractmethod
    def history(self) -> pd.DataFrame: ...

