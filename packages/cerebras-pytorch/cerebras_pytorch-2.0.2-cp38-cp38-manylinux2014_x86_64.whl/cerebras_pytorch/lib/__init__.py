# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

try:
    from . import cerebras_pytorch_lib
except ImportError:
    # In case cerebras_pytorch_pylib is not available we mock
    # it with a dummy class which raises an execption if the
    # library was accessed. At the same time we want to keep
    # this library importable.
    class CatchAllMethodCalls(type):
        def __getattribute__(cls, attr):
            raise Exception(
                "cerebras_pytorch_lib is not supposed to be used in cbcore."
            )

    class cerebras_pytorch_lib(metaclass=CatchAllMethodCalls):
        pass
