from typing import Sequence, SupportsIndex
import numpy as np
import pandas as pd
from swan_testing.soma import Soma
from swan_testing.soma import CurrentSoma
from swan_testing.current_generator import ExpConstCurrent
from swan_testing.current_receiver import FHN
from swan_testing.model_tests.grid import ParamGrid, GridTest
import swan_testing.plotting as stplt


def n_spikes(
    soma: Soma,
    pulses: tuple[Sequence[float], SupportsIndex],
) -> np.int64:
    soma.pulses(*pulses)
    history = soma.history()
    n_spikes = history["spike"].where(history["spike"]).count()
    assert not isinstance(n_spikes, pd.Series)
    return np.int64(n_spikes)


def fhn_act_thresh(
    pulse_magnitude: float,
    ninety_pct_time: float,
    a: float,
    b: float,
    tau: float,
    spike_magnitude: float,
    dt: float,
    time_per_update: float,
) -> np.int64:
    cur_gen = ExpConstCurrent(ninety_pct_time)
    cur_rec = FHN(a, b, tau)
    soma = CurrentSoma(spike_magnitude, cur_gen, cur_rec, dt, time_per_update)
    no_input = ([0.0], int(10 * tau / time_per_update))
    if n_spikes(soma, no_input) > 0:
        return np.int64(1)
    input = ([pulse_magnitude], int(100 / time_per_update))
    if n_spikes(soma, input) > 0:
        return np.int64(0)
    return np.int64(-1)


def main():
    param_grid = ParamGrid({
        "pulse_magnitude": [0.24],
        "ninety_pct_time": [round(5 + 1.0 * x, 5) for x in range(0, 11)],
        "a": [round(0.1 * x, 5) for x in range(4, 15)],
        "b": [round(0.1 * x, 5) for x in range(1, 11)],
        "tau": [12.5],
        "spike_magnitude": [1.0],
        "dt": [0.1],
        "time_per_update": [10.0],
    })
    result = GridTest(param_grid, fhn_act_thresh).run()
    # result = result.reorder_vars("ninety_pct_time", "a", "b")
    stplt.grid_test_heat_maps(
        result,
        "Whether update train induced spikes",
        "spike_hz/update_train",
    )


if __name__ == "__main__":
    main()

