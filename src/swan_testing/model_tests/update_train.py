from typing import Iterable, Sequence
from dataclasses import dataclass
import pandas as pd
from ..soma import Soma


@dataclass(slots=True)
class UpdateTrain:
    soma: Soma
    inputs: Iterable[Sequence[float]]

    def run(self) -> pd.DataFrame:
        return pd.DataFrame()

