from typing import Any, Iterable, Iterator, Mapping, Self, Sequence
from dataclasses import dataclass
from itertools import product


@dataclass(slots=True)
class ParamArray:
    params: dict[str, Any]
    vars: list[tuple[str, list]]

    def __init__(
        self,
        params: Mapping[str, Any],
    ) -> None:
        self.params: dict[str, Any] = {}
        for key, value in params.items():
            if isinstance(value, Mapping):
                self.params[key] = type(self)(value)
                continue
            elif not isinstance(value, Iterable) or isinstance(value, (str, bytes, type(self))):
                self.params[key] = value
                continue
            _value = list(value)
            if len(_value) == 0:
                self.params[key] = None
            elif len(_value) == 1:
                self.params[key] = _value[0]
            else:
                self.params[key] = _value

    # @classmethod
    # def from_nested_dict(
    #     cls,
    #     params: Mapping[str, Self | Sequence[Any] | Mapping],
    # ) -> Self:
    #     parameters: dict[str, Self | Sequence[Any]] = {}
    #     for key, value in params.items():
    #         if isinstance(value, Mapping):
    #             parameters[key] = cls.from_nested_dict(value)
    #         else:
    #             parameters[key] = value
    #     return cls(parameters)

    def __iter__(self) -> Iterator[dict[str, Any]]:
        for condition in product(*self.params.values()):
            yield dict(zip(self.params.keys(), condition))

    @property
    def shape(self) -> tuple[int, ...]:
        shape: tuple[int, ...] = tuple()
        for value in self.params.values():
            if isinstance(value, ParamArray):
                shape += value.shape
            else:
                shape += (len(value),)
        return shape

    @property
    def size(self) -> int:
        return sum(self.shape)

    @property
    def param_vals(self) -> dict[str, list]:
        param_vals: dict[str, list] = {}
        for key, value in self.params.items():
            if isinstance(value, ParamArray):
                param_vals.update(value.param_vals)
            else:
                param_vals[key] = [v for v in value]
        return param_vals

    @property
    def keys(self) -> tuple[str, ...]:
        return tuple(key for key in self.param_vals.keys())

    def reordered_keys(self, *param_keys: str) -> tuple[str, ...]:
        param_indices = {key: index for index, key in enumerate(param_keys)}
        return tuple(
            key
            for key in sorted(
                self.keys,
                key=lambda k: param_indices[k] if k in param_indices else len(self.keys)
            )
        )

    def key_indices(self, *param_keys: str) -> tuple[int, ...]:
        if len(param_keys) == 0:
            param_keys = self.keys
        indices = {key: index for index, key in enumerate(self.keys)}
        return tuple(indices[param_key] for param_key in param_keys)

    def squeeze(self, *param_keys: str) -> tuple[str, ...]:
        if len(param_keys) == 0:
            param_keys = self.keys
        return tuple(key for key in param_keys if len(self.param_vals[key]) > 1)

