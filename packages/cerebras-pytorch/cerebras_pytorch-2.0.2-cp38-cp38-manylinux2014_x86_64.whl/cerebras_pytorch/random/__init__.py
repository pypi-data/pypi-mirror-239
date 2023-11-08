# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""Random number generation helper functions"""
import torch

from ..backend.base_backend import BaseBackend


def manual_seed(seed: int):
    """
    Sets the manual seed for PyTorch as well as the seed used by the backend
    """
    torch.manual_seed(seed)

    BaseBackend.seed = seed
