from typing import Iterable
from dataclasses import dataclass, field
import pandas as pd
from.current_receiver import CurrentReceiver


@dataclass(slots=True)
class FHN(CurrentReceiver):
    a: float
    b: float
    tau: float
    v: float = -1.0
    w: float = -0.5
    v_prev: float = -1.0
    w_prev: float = -0.5
    t: float = 0.0
    log: list[dict[str, float | bool | None]] = field(default_factory=list)

    def update(self, i: float, dt: float) -> bool:
        dv = self.v - self.v ** 3 / 3 - self.w + i
        dw = (self.v + self.a - self.b * self.w) / self.tau
        self.t += dt
        self.v_prev = self.v
        self.w_prev = self.w
        self.v = self.v + dv * dt
        self.w = self.w + dw * dt
        self.update_log((self.t,), (self.v,), (self.w,), (i,), (self.spike_initiated(),))
        return self.spike_initiated()

    def get_v(self) -> float:
        return self.v

    def spike_initiated(self) -> bool:
        return self.v_prev < 1 and self.v >= 1

    def update_log(
        self,
        t_vals: Iterable[float],
        v_vals: Iterable[float],
        w_vals: Iterable[float],
        i_vals: Iterable[float],
        spikes: Iterable[bool],
    ) -> None:
        for t, v, w, i, spike in zip(t_vals, v_vals, w_vals, i_vals, spikes):
            self.log.append({"time": t, "voltage": v, "recovery": w, "current": i, "spike": spike})

    def history(self) -> pd.DataFrame:
        """Get the history of the FHN as a `DataFrame`.
        #
        Returns
        -------
        `history` : `pandas.DataFrame`
            The record of all time steps.
            Columns:
            "time", "voltage", "current", "spike";
            `float`, `float`, `float`, `bool`
        """
        return pd.DataFrame(self.log)


