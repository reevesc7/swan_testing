from typing import Any, Callable, Iterator, Mapping, Self, Sequence, SupportsIndex, TypeVar
from collections import OrderedDict
from dataclasses import dataclass
from itertools import product
import numpy as np


K = TypeVar("K")
V = TypeVar("V")


class IndexDict(OrderedDict[K, V]):
    def index(self, index: SupportsIndex) -> tuple[K, V]:
        key = tuple(self.keys())[index]
        return key, self[key]


@dataclass(slots=True)
class ParamGrid:
    vars: IndexDict[str, Sequence]
    consts: IndexDict[str, Any]

    def __init__(
        self,
        params: Mapping[str, Sequence],
    ) -> None:
        self.vars: IndexDict[str, Sequence] = IndexDict()
        self.consts: IndexDict[str, Any] = IndexDict()
        for key, value in params.items():
            if len(value) == 1:
                self.consts[key] = value[0]
            else:
                self.vars[key] = value

    @classmethod
    def _raw_init(
        cls,
        vars: IndexDict[str, Sequence],
        consts: IndexDict[str, Any],
    ) -> Self:
        grid = cls({})
        grid.vars = vars
        grid.consts = consts
        return grid

    def __iter__(self) -> Iterator[IndexDict[str, Any]]:
        for params in product(*self.vars.values()):
            yield IndexDict(zip(self.vars.keys(), params)) | self.consts

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(len(value) for value in self.vars.values())

    @property
    def size(self) -> int:
        return sum(self.shape)

    def reorder_vars(self, *param_keys: str, last: bool = False) -> Self:
        if len(param_keys) == 0:
            param_keys = tuple(reversed(self.vars.keys()))
        vars = self.vars.copy()
        if not last:
            param_keys = tuple(reversed(param_keys))
        for key in param_keys:
            vars.move_to_end(key, last=False)
        return type(self)._raw_init(vars, self.consts)

    def var_key_indices(self, *param_keys: str) -> tuple[int, ...]:
        if len(param_keys) == 0:
            param_keys = tuple(self.vars.keys())
        indices = {key: index for index, key in enumerate(self.vars.keys())}
        return tuple(indices[param_key] for param_key in param_keys)


@dataclass(slots=True)
class GridTestResult:
    param_grid: ParamGrid
    data: np.ndarray

    def __iter__(self) -> Iterator[tuple[IndexDict[str, Any], Any]]:
        for index, params in enumerate(product(*self.vars.values())):
            yield IndexDict(zip(self.vars.keys(), params)), self.data.flat[index]

    @property
    def vars(self) -> IndexDict[str, Sequence]:
        return self.param_grid.vars

    @property
    def consts(self) -> IndexDict[str, Any]:
        return self.param_grid.consts

    @property
    def shape(self) -> tuple[int, ...]:
        return self.param_grid.shape

    def nditer(
            self,
            n_dims: SupportsIndex,
    ) -> Iterator[tuple[IndexDict[str, Any], IndexDict[str, Sequence], np.ndarray | Any]]:
        vars_items = tuple(self.vars.items())
        iter = IndexDict(vars_items[:n_dims])
        extra = IndexDict(vars_items[n_dims:])
        for params, data_index in zip(product(*iter.values()), np.ndindex(self.data.shape[:n_dims])):
            yield IndexDict(zip(iter.keys(), params)), extra, self.data[data_index]

    def var_key_indices(self, *param_keys: str) -> tuple[int, ...]:
        return self.param_grid.var_key_indices(*param_keys)

    def reorder_vars(self, *param_keys: str, last: bool = False) -> Self:
        param_array = self.param_grid.reorder_vars(*param_keys, last=last)
        data = np.transpose(self.data, self.var_key_indices(*self.vars.keys()))
        return type(self)(param_array, data)


@dataclass(slots=True)
class GridTest:
    param_grid: ParamGrid
    func: Callable

    def run(self) -> GridTestResult:
        data = np.empty(self.param_grid.shape)
        for condtn_index, params in enumerate(self.param_grid):
            data.flat[condtn_index] = self.func(**params)
        return GridTestResult(self.param_grid, data)

