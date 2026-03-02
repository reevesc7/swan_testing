from typing import Iterable
from dataclasses import dataclass, field
# from math import ceil
import pandas as pd
# from .current import CurrentGenerator, NullCurrentGenerator
from.current_receiver import CurrentReceiver


@dataclass(slots=True)
class FHN(CurrentReceiver):
    a: float
    b: float
    tau: float
    # current_generator: CurrentGenerator = field(default_factory=NullCurrentGenerator)
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

    # def next_v(self, i: float, dt: float) -> float:
    #     # i += self.current_generator.next_i(self.v, dt)
    #     dv = self.v - self.v ** 3 / 3 - self.w + i
    #     dw = self.epsilon * (self.v + self.a - self.b * self.w)
    #     self.t += dt
    #     self.v_prev = self.v
    #     self.w_prev = self.w
    #     self.v = self.v + dt * dv
    #     self.w = self.w + dt * dw
    #     self.update_history((self.t,), (self.v,), (i,), (self.spike_initiated(),))
    #     return self.v

    def spike_initiated(self) -> bool:
        return self.v_prev < 1 and self.v >= 1

    # def constant_current(self, time: float, i: float) -> None:
    #     """Run the FHN for a given time with a given input current.
    #     #
    #     Parameters
    #     ----------
    #     `time` : `float`
    #         The amount of time units to run for. Number of time steps this results in
    #         depends on `self.dt`.
    #     `i` : `float`
    #         The input current, provided on each time step.
    #     """
    #     time_steps = ceil(time / self.dt)
    #     for _ in range(time_steps):
    #         self.next_v(i)
    #
    # def spin(self, time: float) -> None:
    #     """Spin the FHN's wheels, inputting 0.0 current for given time.
    #     """
    #     self.constant_current(time, 0.0)
    #
    # def current_segments(self, time_vals: Iterable[float], i_vals: Iterable[float]) -> None:
    #     """Run the FHN for a set of given times with given input currents.
    #     #
    #     Parameters
    #     ----------
    #     `time_vals` : `Iterable[float]`
    #         The duration of each segment.
    #         Number of time steps this results in depends on `self.dt`.
    #     `i_vals` : `Iterable[float]`
    #         The input current of each segment.
    #     """
    #     for time, i in zip(time_vals, i_vals):
    #         self.constant_current(time, i)
    #
    # def current_train(self, i_vals: Iterable[float]) -> None:
    #     """Run the FHN over a set of time steps with given input currents.
    #     #
    #     Parameters
    #     ----------
    #     `i_vals` : `Iterable[float]`
    #         The input current of time step.
    #     """
    #     for i in i_vals:
    #         self.next_v(i)
    #
    # def input_pulse(self, magnitude: float) -> None:
    #     self.history[-1]["pulse"] = magnitude
    #     self.current_generator.input_pulse(magnitude)
    #
    # def pulse_train(self, time_vals: Iterable[float], magnitude_vals: Iterable[float]) -> None:
    #     """Run the FHN for a set of given times with pulses given at each segment.
    #     #
    #     Parameters
    #     ----------
    #     `time_vals` : `Iterable[float]`
    #         The duration of each segment.
    #         Number of time steps this results in depends on `self.dt`.
    #     `magnitude_vals` : `Iterable[float]`
    #         The magnitude of the pulse of each segment.
    #         Pulses are given at the start of each segment.
    #     """
    #     for time, magnitude in zip(time_vals, magnitude_vals):
    #         self.input_pulse(magnitude)
    #         self.spin(time)

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


