# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""
The revamped Cerebras PyTorch package
"""
import os

import torch

# True if we're autogenerating docs
# This environment variable should only ever be set in the documentation repository
# when autogenerating docs from the docstrings in this package
_generating_docs = bool(
    os.environ.get("GENERATING_CEREBRAS_PYTORCH_DOCS") == "1"
)

# pylint: disable=redefined-builtin
from .backend import backend, current_backend, current_torch_device, use_cs
from .core.compile import compile, trace
from .core.name_scope import (
    add_debug_name,
    get_debug_name,
    name_scope,
    set_debug_scope,
)
from .random import manual_seed
from .saver import load, save
from .saver.storage import full, full_like, ones, ones_like, zeros, zeros_like
from .utils.constant import make_constant
from .utils.data.utils import from_numpy, to_numpy
from .utils.step_closures import checkpoint_closure, step_closure
from .utils.tensorboard import summarize_scalar, summarize_tensor

# isort: off
from . import amp, core, distributed, metrics, nn, optim, sparse, utils

# isort: on

__all__ = [
    "amp",
    "backend",
    "checkpoint_closure",
    "compile",
    "trace",
    "current_backend",
    "current_torch_device",
    "from_numpy",
    "full",
    "full_like",
    "load",
    "manual_seed",
    "metrics",
    "nn",
    "ones",
    "ones_like",
    "optim",
    "save",
    "step_closure",
    "summarize_scalar",
    "summarize_tensor",
    "to_numpy",
    "use_cs",
    "utils",
    "zeros",
    "zeros_like",
]


cirh = torch.ops.cirh

if not _generating_docs:
    from ._version import __version__
    from .lib import cerebras_pytorch_lib
else:
    # There will be no version file when generating docs
    __version__ = None
    cerebras_pytorch_lib = None
