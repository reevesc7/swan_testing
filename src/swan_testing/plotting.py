from typing import Iterator, Sequence
from itertools import product
import textwrap
import numpy as np
from numpy.typing import ArrayLike
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from .model_tests.grid import GridTestResult


def plot_axes(
    ax: Axes,
    title: str,
    xlabel: str,
    ylabel: str,
) -> Axes:
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


# def v_i_spikes(
#     ax: Axes,
#     t_vals: ArrayLike,
#     v_vals: ArrayLike,
#     w_vals: ArrayLike,
#     i_vals: ArrayLike,
#     spikes: ArrayLike,
#     title: str,
#     axis_labels: tuple[str, str],
# ) -> Axes:
#     """Plot voltage and detected spike events over time.
#     #
#     Parameters
#     ----------
#     `ax` : `matplotlib.axes.Axes`
#         An axes on which to plot. Mutated and returned by this function.
#     `t_vals` : `ArrayLike`
#         Array of time steps.
#     `v_vals` : `ArrayLike`
#         Array of voltage at time steps.
#     `i_vals` : `ArrayLike`
#         Array of current at time steps.
#     `spikes` : `ArrayLike`
#         Array of booleans, `True` at time steps a spike occured.
#     `title` : `str`
#         Title for the plot.
#     `axis_labels` : `tuple[str, str]`
#         x-label and y-label for the plot.
#     #
#     Returns
#     -------
#     `axes` : `matplotlib.axes.Axes`
#         The axes, with voltage, current, and spike events plotted over time.
#     """
#     t_vals = np.asarray(t_vals)
#     v_vals = np.asarray(v_vals)
#     w_vals = np.asarray(w_vals)
#     i_vals = np.asarray(i_vals)
#     spikes = np.asarray(spikes)
#     ax = plot_axes(ax, title, axis_labels[0], axis_labels[1])
#     ax.plot(t_vals, w_vals, color="blue", alpha=0.5)
#     ax.plot(t_vals, i_vals, color="limegreen", alpha=0.5)
#     for t in t_vals[spikes]:
#         ax.axvline(t, color="red", alpha=0.5)
#     ax.plot(t_vals, v_vals, color="black")
#     return ax


def heat_map_axes(
    ax: Axes,
    title: str,
    xlabel: str,
    ylabel: str,
    xticklabels: Sequence[str],
    yticklabels: Sequence[str],
) -> Axes:
    ax.set_xticks(
        range(len(xticklabels)),
        labels=xticklabels,
        rotation=45,
        ha="right",
        rotation_mode="anchor",
    )
    ax.set_yticks(range(len(yticklabels)), labels=yticklabels)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


# def heat_map(
#     ax: Axes,
#     data: ArrayLike,
#     x_ticklabels: Sequence[str],
#     y_ticklabels: Sequence[str],
#     title: str,
#     axis_labels: tuple[str, str],
#     map_labels: bool = False,
# ) -> Axes:
#     data = np.asarray(data)
#     ax = heat_map_axes(ax, title, axis_labels[0], axis_labels[1], x_ticklabels, y_ticklabels)
#     ax.imshow(data.T)
#     if not map_labels:
#         return ax
#     for x, y in product(range(len(x_ticklabels)), range(len(y_ticklabels))):
#         ax.text(x, y, str(int(data[y, x])), ha="center", va="center", color="white")
#     return ax


def grid_test_heat_maps(result: GridTestResult, title: str, filename: str) -> None:
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25)
    fig_text = fig.text(
        0.01,
        0.01,
        "",
        ha="left",
        va="bottom",
        fontsize=8,
        family="monospace",
    )
    ax = heat_map_axes(
        ax,
        title,
        xlabel=result.vars.index(-2)[0],
        ylabel=result.vars.index(-1)[0],
        xticklabels=[str(v) for v in result.vars.index(-2)[1]],
        yticklabels=[str(v) for v in result.vars.index(-1)[1]],
    )
    heat_map = ax.imshow(np.zeros(result.shape[-2:]).T)
    heat_map.set_clim(vmin=-1, vmax=1)
    for index, (map_consts, _, map_data) in enumerate(result.nditer(-2)):
        consts = map_consts | result.consts
        consts_label = ", ".join(
            f"{k}: {v}" if not isinstance(v, Sequence) else f"len({k}): {len(v)}"
            for k, v in consts.items()
        )
        fig_text.set_text("\n".join(textwrap.wrap(consts_label, 93)))
        map_data = np.asarray(map_data)
        heat_map.set_data(map_data.T)
        fig.savefig(f"{filename}_{index}")
    plt.close(fig)


# def multi_heat_map(
#     ax: Axes,
#     data: ArrayLike,
#     x_ticklabels: Sequence[str],
#     y_ticklabels: Sequence[str],
#     title: str,
#     axis_labels: tuple[str, str],
#     map_labels: bool = False,
# ) -> Iterator[Axes]:
#     data = np.asarray(data)
#     for map in np.ndindex(data.shape[:-2]):
#         yield heat_map(
#             ax,
#             data[map],
#             x_ticklabels,
#             y_ticklabels,
#             title,
#             axis_labels,
#             map_labels,
#         )

