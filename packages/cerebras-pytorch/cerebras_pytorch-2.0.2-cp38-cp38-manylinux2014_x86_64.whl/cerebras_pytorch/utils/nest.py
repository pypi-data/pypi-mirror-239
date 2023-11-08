# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

from typing import Any, Callable, Generator, List, Optional, Tuple, Union

import torch
from torch.utils._pytree import TreeSpec, tree_flatten, tree_unflatten

TScope = List[str]
TNested = Union[Any, list, tuple, dict]
TSelectFn = Callable[[Any], bool]


def visit_structure(
    data_structure: TNested,
    select_fn: TSelectFn,
    strict: bool = False,
    scope: Optional[TScope] = None,
) -> Generator[Tuple[TScope, Any], None, None]:
    """Recursively traverse nested structure and return the items accepted by
    the selector.

    Args:
        data_structure: A nested data structure to traverse recursively.
        select_fn: A callable that returns true if the item passed should be
            selected.
        strict: Strictly checks that an item in the nested structure is either
            a list/dict/tuple or selected by the select_fn. Otherwise, raises
            an error. Defaults to False.
        scope: The current hierarchical scope of the data structure. Defaults
            to None.
    Yields:
        A tuples of (scope, item) for each item selected by the select_fn.
    """
    scope = scope or []
    if isinstance(data_structure, (list, tuple)):
        for i, v in enumerate(data_structure):
            yield from visit_structure(v, select_fn, strict, scope + [str(i)])
    elif isinstance(data_structure, dict):
        for k, v in data_structure.items():
            yield from visit_structure(v, select_fn, strict, scope + [str(k)])
    elif select_fn(data_structure):
        yield scope, data_structure
    elif strict:
        raise ValueError(f"Unknown data structure: {data_structure}")


def visit_torch_tensors(
    data_structure: TNested,
    strict: bool = False,
    scope: Optional[TScope] = None,
):
    """Recursively finds all torch tensors in the nested data structure.

    Args:
        data_structure: A nested data structure to traverse recursively.
        strict: Strictly checks that an item in the nested structure is one of
            a list/dict/tuple/tensor. Otherwise, raises an error. Defaults to
            False.
        scope: The current hierarchical scope of the data structure. Defaults
            to None.
    Yields:
        A tuple of (scope, tensor) for each tensor in the nested structure.
    """
    yield from visit_structure(
        data_structure,
        select_fn=lambda item: isinstance(item, torch.Tensor),
        strict=strict,
        scope=scope,
    )


def visit_device_tensors(
    data_structure: TNested,
    device_type: str,
    strict: bool = False,
    scope: Optional[TScope] = None,
):
    """Recursively finds all device tensors in the nested data structure.

    Args:
        data_structure: A nested data structure to traverse recursively.
        strict: Strictly checks that an item in the nested structure is one of
            a list/dict/tuple/device tensor. Otherwise, raises an error.
            Defaults to False.
        scope: The current hierarchical scope of the data structure. Defaults
            to None.
    Yields:
        A Tuple of (scope, tensor) for each tensor in the nested structure.
    """
    for s, tensor in visit_torch_tensors(
        data_structure, strict=strict, scope=scope,
    ):
        if tensor.device.type == device_type:
            yield s, tensor


def visit_lazy_tensors(
    data_structure: TNested,
    strict: bool = False,
    scope: Optional[TScope] = None,
):
    """Recursively finds all Lazy tensors in the nested data structure.

    Args:
        data_structure: A nested data structure to traverse recursively.
        strict: Strictly checks that an item in the nested structure is one of
            a list/dict/tuple/Lazy tensor. Otherwise, raises an error. Defaults
            to False.
        scope: The current hierarchical scope of the data structure. Defaults
            to None.
    Yields:
        A Tuple of (scope, Lazy tensor) for each tensor in the nested structure.
    """
    yield from visit_structure(
        data_structure,
        select_fn=lambda item: isinstance(item, torch.Tensor)
        and item.device.type == "lazy",
        strict=strict,
        scope=scope,
    )


def map_structure(
    map_fn: Callable,
    data_structure: TNested,
    select_fn: TSelectFn,
    scope: Optional[TScope] = None,
):
    objs, spec = tree_flatten(data_structure)

    objs = [
        map_fn(s, t) if select_fn(t) else t
        for s, t in zip(recurse_spec(spec, scope), objs)
    ]
    return tree_unflatten(objs, spec)


def map_torch_tensors(
    map_fn: Callable, data_structure: TNested, scope: Optional[TScope] = None,
):
    return map_structure(
        map_fn,
        data_structure,
        select_fn=lambda item: isinstance(item, torch.Tensor),
        scope=scope,
    )


def map_lazy_tensors(
    map_fn: Callable, data_structure: TNested, scope: Optional[TScope] = None,
):
    return map_structure(
        map_fn,
        data_structure,
        select_fn=lambda item: isinstance(item, torch.Tensor)
        and item.device.type == "lazy",
        scope=scope,
    )


def recurse_spec(spec: TreeSpec, scope: Optional[TScope] = None):
    if spec.num_leaves == 0:
        return

    scope = scope or []
    if spec.context:
        for key, val in zip(spec.context, spec.children_specs):
            yield from recurse_spec(val, scope + [str(key)])
    elif not spec.children_specs:
        yield scope
    else:
        for i, val in enumerate(spec.children_specs):
            yield from recurse_spec(val, scope + [str(i)])
