# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

""" Cerebras specific subclass of torch.nn.Parameter """
import warnings
from typing import Optional

import torch

from cerebras_appliance.saver.h5_saver import register_h5_type
from cerebras_pytorch.backend import current_backend_impl
from cerebras_pytorch.saver.pt_h5_saver import TorchTensorH5Type
from cerebras_pytorch.saver.storage import lazy_tensor_data_wrapper


class Parameter(torch.nn.Parameter):
    """
    Cerebras specific subclass of torch.nn.Parameter
    """

    def __new__(cls, data=None):  # pylint: disable=signature-differs
        assert isinstance(data, torch.Tensor)

        if isinstance(data, Parameter):
            return data

        # pylint: disable=protected-access,attribute-defined-outside-init
        return torch.Tensor._make_subclass(cls, data, data.requires_grad)

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._lazy_param: Optional[Parameter] = None
        self._cpu_param: Optional[Parameter] = None

    def copy_(self, tensor: torch.Tensor) -> torch.Tensor:
        """Copy the tensor into this parameter.

        This overrides the default copy_() method to handle copying tensors with
        storage onto this parameter. This is needed because the default copy_()
        method only traces the "copy_()" op. However, for cases where we're
        loading a checkpoint tensor into this parameter, we want to copy actual
        storage instead of tracing.
        """
        if self.device.type == "lazy" and (
            not current_backend_impl().is_tracing
        ):
            _lazy_copy_storage(self, tensor)
            # Clear the CPU param since we've replaced the underlying storage
            self._cpu_param = None
        else:
            super().copy_(tensor)

        return self

    def clone(self, *args, **kwargs) -> "Parameter":
        if self.device.type == "cpu":  # pylint: disable=no-member
            assert self._lazy_param is not None
            cloned = self._lazy_param.clone()
            cloned.requires_grad = self.requires_grad
            return cloned.to("cpu")
        elif self.device.type == "lazy":
            from cerebras_pytorch.lib import cerebras_pytorch_lib

            if not current_backend_impl().is_tracing:
                cloned = Parameter(
                    cerebras_pytorch_lib.clone_tensor(self._data)
                )
                cloned.requires_grad = self.requires_grad
                return cloned
            else:
                return super().clone(*args, **kwargs)
        else:
            raise RuntimeError(
                f"Unsupported device type: {self.device.type}. Expected one of "
                f"\"cpu\" or \"lazy\"."
            )

    def __deepcopy__(self, memo: dict) -> "Parameter":
        return memo.setdefault(id(self), self.clone())

    def detach(self):
        return self

    def get_lazy_data(self):
        """
        Overrides Parameter data property to handle parameter.data access for cases when lazy device is used.
        This is a workaround for LTC + drop_data (validate_only/compile_only mode) to support cases when
        parameter has indirect inplace update via p.data.op_(...).

        Let's take a look at the example:

            >>> p = torch.nn.Parameter(torch.ones((3)))
            >>> p = p.to("lazy")
            >>> a.normal_()

            This code will behave exaclty how we expect, so inplace normal_ op will update parameter
            with new lazy tensor. But if we apply inplace operation to the data tensor:

            >>> a.data.normal_()

            so it will produce new lazy tensor, but the tensor inside parameter won't be updated and remains
            the same which is crucial for drop_data case where we want to trace initialization sub-graph and
            we need to keep lazy tensor inside parameters in sync with ltc tracing.

        But as the goal of drop_data and initialization sub-graph tracing with lazy tensors is to drop resulting
        graph, we can easily fix this desynchronization of parameters and lazy tensors by returning dummy meta
        tensor when p.data is being accessed.
        """
        if not current_backend_impl().is_tracing:
            return torch.empty(self.shape, dtype=self.dtype, device="meta")
        else:
            raise RuntimeError(
                "Accessing \".data\" of torch parameter is not supported during tracing. Please update the parameter directly "
                "instead of updating the underlying tensor."
            )

    def set_lazy_data(self, name, value):
        if not current_backend_impl().is_tracing:
            # Drop data.
            return
        else:
            raise RuntimeError(
                "Accessing \".data\" of torch parameter is not supported during tracing. Please update the parameter directly "
                "instead of updating the underlying tensor."
            )

    def __getattribute__(self, name):
        if name == "data" and self.device.type == "lazy":
            return self.get_lazy_data()

        # For some cases in Parameter methods we still need an acces to original data. So
        # as a workaround  we call self._data which bypass self.data access logic.
        if name == "_data":
            name = "data"

        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == "data" and self.device.type == "lazy":
            return self.set_lazy_data(name, value)

        # Symmetric method to set data using self._data=value to original tensor data field.
        if name == "_data":
            name = "data"

        return super().__setattr__(name, value)

    def to(self, *args, **kwargs):
        # pylint: disable=protected-access
        device, dtype, non_blocking, memory_format = torch._C._nn._parse_to(
            *args, **kwargs
        )
        # TODO: Error out if dtype, non_blocking, or memory_format are specified

        if device is None:
            pass
        elif device.type != self.device.type:  # pylint: disable=no-member
            if device.type != "cpu":  # pylint: disable=no-member
                assert self._lazy_param is not None
                # User may have modified the parameter since we captured
                # _lazy_param, so update the replacement to keep it consistent
                self._lazy_param.requires_grad = self.requires_grad
                # Clear the CPU param to release virtual memory in case of
                # file-backed appliance data. This is needed to avoid OOM errors
                # during python subprocess forking.
                self._lazy_param._cpu_param = None

                return self._lazy_param
            else:
                if self._cpu_param is not None:
                    # User may have modified the parameter since we captured
                    # _lazy_param, so update the replacement to keep it consistent
                    self._cpu_param.requires_grad = self.requires_grad
                    return self._cpu_param

                if self.device.type == "lazy":
                    from cerebras_pytorch.lib import cerebras_pytorch_lib

                    data = cerebras_pytorch_lib.get_appliance_data(self._data)
                    try:
                        tensor = data.tensor
                    except RuntimeError:
                        backend = current_backend_impl()
                        if backend.device.drop_data:
                            # In compile only, we actually discard app data to
                            # save memory. However, we may need the metadata of
                            # the tensor, so return an empty tensor like it.
                            tensor = torch.empty_like(self, device=device)
                        else:
                            # Otherwise, that was a valid error...
                            raise
                    cpu_param = Parameter(tensor)
                    cpu_param.requires_grad = self.requires_grad
                else:
                    cpu_param = super().to(*args, **kwargs)

                # pylint: disable=protected-access,attribute-defined-outside-init
                cpu_param._lazy_param = self

                self._cpu_param = cpu_param
                return cpu_param
        else:
            return self

        return super().to(*args, **kwargs)

    def __repr__(self):
        if self.device.type != "cpu":
            warnings.warn(
                "Parameter repr may not contain actual stored values. "
                "Move the tensor to cpu via .to(\"cpu\") to view real values."
            )
        return super().__repr__()

    def __str__(self):
        if self.device.type != "cpu":
            warnings.warn(
                "Parameter str may not contain actual stored values. "
                "Move the tensor to cpu via .to(\"cpu\") to view real values."
            )
        return super().__str__()


class Buffer(torch.Tensor):
    """A lazy tensor wrapper for module buffers.

    This class wraps a lazy tensor and overrides the `copy_()` method to copy
    the data when loading a checkpoint as opposed to the default behavior of
    tracing the copy operation.
    """

    __torch_function__ = torch._C._disabled_torch_function_impl

    def __new__(cls, elem: torch.Tensor):
        assert isinstance(elem, torch.Tensor) and elem.device.type == "lazy"
        return cls._make_subclass(cls, elem, require_grad=elem.requires_grad)

    def copy_(self, tensor: torch.Tensor) -> torch.Tensor:
        if current_backend_impl().is_tracing:
            return super().copy_(tensor)
        return _lazy_copy_storage(self, tensor)


# Register the custom classes for saving via H5Saver
register_h5_type(Parameter)(TorchTensorH5Type)
register_h5_type(Buffer)(TorchTensorH5Type)


def _lazy_copy_storage(
    self: torch.Tensor, tensor: torch.Tensor
) -> torch.Tensor:
    """Copies the data from `tensor` into `self` without tracing.

    This is to handle 2 cases where we want to copy storage instead of tracing:
    1. Copying a CPU tensor into a lazy parameter. This can happen
       when we load a vanilla torch checkpoint onto CPU and then
       load it into a lazy parameter.
    2. Copying a DeferredTensor into a lazy parameter. This can happen
       when we load an H5 checkpoint onto the lazy device and then
       load it into a lazy parameter.

    Args:
        self: The lazy tensor to copy into.
        tensor: The tensor to copy from.
    Returns:
        self.
    """
    from cerebras_pytorch.lib import cerebras_pytorch_lib

    if not isinstance(tensor, torch.Tensor):
        raise RuntimeError(
            f"Attempting to copy a non-tensor type {type(tensor)} into a "
            f"tensor."
        )

    if self.shape != tensor.shape:
        raise RuntimeError(
            f"Cannot copy tensor of different shape ({tensor.shape}) "
            f"into a lazy buffer with shape {self.shape}."
        )

    if self.dtype != tensor.dtype:
        # If the dtype is different we need to get the data wrapper
        # and convert the tensor to the correct dtype before copying.
        # Note, for deferred tensors, this will involve an extra
        # read and write to disk, but this should be rare as most
        # cases should be handled by the checkpoint converter
        tensor = lazy_tensor_data_wrapper(tensor)
        tensor = tensor.type(self.dtype)

    # Currently a vanilla torch checkpoint is loaded onto CPU, so we need
    # to handle copying from a CPU tensor to a lazy tensor.
    if isinstance(tensor, torch.Tensor) and tensor.device.type == "cpu":
        from cerebras_pytorch.backend import current_backend

        with current_backend().device:
            lazy_tensor = tensor.to("lazy")
    else:
        lazy_tensor = tensor

    # lazy tensor `copy_()` traces the op and doesn't actually copy the
    # underlying storage. But we want to copy the ApplianceData storage
    # through sharing data with the `lazy_tensor`.
    cerebras_pytorch_lib.copy_appliance_data(
        lazy_tensor, self._data if isinstance(self, Parameter) else self.data
    )

    return self
