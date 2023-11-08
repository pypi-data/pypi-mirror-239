# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""
PyTorch Device configuration
"""

import atexit
import os
import sys

from cerebras_appliance import register_deps
from cerebras_pytorch.utils.call_once import call_once


def _initialize_error():
    raise RuntimeError(
        "Initializing cstorch multiple times from the same "
        "process is not supported. "
        "Initializing multiple times can cause unexpected bugs "
        "and unsupported behaviours with the way that PyTorch "
        "load their dynamic libraries."
    )


@call_once(error_callable=_initialize_error)
def _initialize_ltc(verbose: bool = False, debug: bool = False):
    """Initialize unconditionally only if LTC path is enabled"""

    from cerebras_pytorch.lib import cerebras_pytorch_lib

    # pylint: disable=c-extension-no-member
    cerebras_pytorch_lib.initialize(ir_debug=debug)
    atexit.register(cerebras_pytorch_lib.shutdown)

    register_deps(
        {
            "cerebras-pytorch": "cerebras_pytorch",
            "torch": "torch",
            "torchvision": "torchvision",
        },
    )

    if debug:
        os.environ["LTC_IR_DEBUG_ROOT_PATH"] = ":".join(
            # sys.path entries in order from longest to shortest
            sorted(
                (path + "/" for path in sys.path if path), key=lambda x: -len(x)
            )
        )
