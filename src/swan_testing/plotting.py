from typing import Sequence
import textwrap
import numpy as np
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


def save_grid_heat_maps(
    result: GridTestResult,
    title: str,
    filename: str,
) -> None:
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
            f"{k}: {v}" if not isinstance(v, Sequence) or len(v) < 10 else f"len({k}): {len(v)}"
            for k, v in consts.items()
        )
        fig_text.set_text("\n".join(textwrap.wrap(consts_label, 93)))
        map_data = np.asarray(map_data)
        heat_map.set_data(map_data.T)
        fig.savefig(f"{filename}_{index}")
    plt.close(fig)

