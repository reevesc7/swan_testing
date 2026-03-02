from typing import Iterable, Sequence, SupportsIndex
import textwrap
import matplotlib.pyplot as plt
from swan_testing.soma import CurrentSoma
from swan_testing.current_generator import ExpConstCurrent
from swan_testing.current_receiver import FHN
import swan_testing.plotting as stplt


def plot_soma(
    pulses_segments: Iterable[tuple[Sequence[float], SupportsIndex]],
    ninety_pct_time: float,
    a: float,
    b: float,
    tau: float,
    spike_magnitude: float,
    dt: float,
    time_per_update: float,
) -> None:
    cur_gen = ExpConstCurrent(ninety_pct_time)
    cur_rec = FHN(a, b, tau)
    soma = CurrentSoma(spike_magnitude, cur_gen, cur_rec, dt, time_per_update)
    soma.pulses_segments(pulses_segments)
    data = soma.history()
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25)
    text = f"pulses_segments: {pulses_segments}, a: {a}, b: {b}, tau: {tau}, dt: {dt}, time_per_update: {time_per_update}"
    fig.text(
        0.01,
        0.01,
        "\n".join(textwrap.wrap(text, 93)),
        ha="left",
        va="bottom",
        fontsize=8,
        family="monospace",
    )
    ax = stplt.plot_axes(
        ax,
        title=f"Voltage, recovery, current, and spikes over time",
        xlabel="time",
        ylabel="voltage",
    )
    ax.plot(data["time"], data["recovery"], color="blue", alpha=0.5)
    ax.plot(data["time"], data["current"], color="limegreen", alpha=0.5)
    for t in data["time"][data["spike"]]:
        ax.axvline(t, color="red", alpha=0.5)
    ax.plot(data["time"], data["voltage"], color="black")
    fig.savefig("soma_plot")
    plt.close(fig)


def main():
    plot_soma(
        pulses_segments=[([0.0], 4), ([0.16], 8), ([0.0], 1), ([0.16], 4)],
        ninety_pct_time=5.0,
        a=0.7,
        b=0.8,
        tau=12.5,
        spike_magnitude=1.0,
        dt=0.1,
        time_per_update=10.0,
    )


if __name__ == "__main__":
    main()

