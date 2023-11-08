# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""
PyTorch specific overrides for saving a state dict to a
Cerebras H5 based checkpoint
"""
from contextlib import nullcontext
from typing import Type, Union

import dill
import h5py as h5
import torch

import cerebras_pytorch as cstorch
from cerebras_appliance.saver.h5_saver import (
    H5Saver,
    NumpyArrayH5Type,
    UnknownH5TypeError,
    register_h5_type,
)
from cerebras_pytorch.utils.nest import recurse_spec


class PyTorchH5Saver(H5Saver):
    """
    A PyTorch specific H5Saver subclass
    """

    # The key at which the state dict's spec is saved
    __spec__ = "__spec__"
    # The current version number of our custom checkpoint format
    # Assume any checkpoints without a version number to have version 0.1
    __version__ = 0.4
    __version_key__ = "__version__"

    @classmethod
    def extract_version(cls, fp: Union[str, h5.File]) -> float:
        ctx = nullcontext(fp) if isinstance(fp, h5.File) else h5.File(fp, "r")
        with ctx as f:
            return f.attrs.get(cls.__version_key__, 0.1)

    @classmethod
    def check_version(cls, checkpoint_file: str):
        """
        Check the checkpoint format version and raise a warning or error
        if the version found is different from the current version

        Args:
            checkpoint_file: The path to the checkpoint to check
        """
        version = cls.extract_version(checkpoint_file)

        if version < cls.__version__:
            cls.logger.debug(
                f"Using an older checkpoint format {version} "
                f"(current version: {cls.__version__}). "
                f"Using it to load the state dict may cause unexpected behaviour."
            )
        elif version > cls.__version__:
            raise RuntimeError(
                f"Cannot load checkpoint with format version {version} as "
                f"it is newer than the currently supported format {cls.__version__}"
            )

    @staticmethod
    def flatten_state_dict(state_dict: dict):
        """
        Returns a flattened dictionary where the keys are the compressed scope.
        By definition, the dictionary has depth 1

        Args:
            state_dict: The nested dictionary to flatten
        """
        # pylint: disable=protected-access
        flattened, spec = torch.utils._pytree.tree_flatten(state_dict)
        state_dict = {
            ".".join(scope): v
            for scope, v in zip(recurse_spec(spec), flattened)
        }
        return state_dict, spec

    # pylint: disable=arguments-renamed
    def save(self, ckpt_file: str, state_dict: dict):
        flattened, spec = self.flatten_state_dict(state_dict)

        # Save the spec before saving the rest in case something goes wrong
        self.save_spec(ckpt_file, spec)

        super().save(ckpt_file, flattened)

    def save_tensor(
        self, ckpt_file: str, tensor_name: str, tensor_value: torch.Tensor,
    ):
        # This override is not useless, it skips calling self.save() which would
        # otherwise call save_spec and destroy it
        super().save(ckpt_file, {tensor_name: tensor_value})

    def save_spec(self, ckpt_file, spec):
        """
        Saves the tensor spec to the checkpoint file

        Args:
            ckpt_file: The path to the checkpoint to save the spec to
            spec: The spec object produced by the call to flatten_state_dict
        """
        with h5.File(ckpt_file, "a") as f:
            f.attrs[self.__spec__] = dill.dumps(spec).hex()
            f.attrs[self.__version_key__] = self.__version__

    def _load_tensor_from_checkpoint(self, f: h5.File, key: str):
        try:
            return super()._load_tensor_from_checkpoint(f, key)
        except UnknownH5TypeError:
            pass

        # If the key does not have an H5Type, then it must be from a
        # checkpoint saved in a release 1.8 or lower.
        # The following loading code is only needed for backwards compatibility

        from .storage import (
            DeferredFileTensor,
            DeferredFullTensor,
            DeferredH5Tensor,
            _np_to_torch_dtype,
        )

        dset = f[key]

        if dset.attrs.get("filepath") is not None:
            import torch

            filepath = dset.attrs["filepath"]
            shape = torch.Size(dset.attrs["shape"])
            dtype = dill.loads(bytes.fromhex(dset.attrs["dtype"]))

            return DeferredFileTensor(filepath, shape, dtype)

        # Keep the following loading code for backwards compatibility
        elif dset.attrs.get("is_constructible", False):
            shape = torch.Size(dset.attrs.get("shape"))
            dtype = _np_to_torch_dtype(dset.dtype)
            fill_value = dset.attrs.get("fill_value")

            return DeferredFullTensor(shape, dtype, fill_value)

        elif dset.attrs.get("is_none", False):
            return None
        elif dset.attrs.get("is_string", False):
            return dset.attrs.get("string_val")
        else:
            tensor = DeferredH5Tensor(f.filename, key)

            if dset.attrs.get("is_scalar", False):
                return tensor.to("cpu").item()
            return tensor

    def _load_by_typename(self, h5_type_name: str, f: h5.File, key: str):
        """Load the value using the given H5Type class"""
        # If checkpoint version is <= 0.3, then we assume that all numpy arrays
        # are torch tensors. This is because in previous releases, we saved
        # torch tensors as numpy arrays.
        if h5_type_name == NumpyArrayH5Type.__name__ and (
            self.extract_version(f) <= 0.3
        ):
            return TorchTensorH5Type.load(f, key)
        return super()._load_by_typename(h5_type_name, f, key)


@register_h5_type(torch.Tensor)
class TorchTensorH5Type:
    """
    Class for saving and loading PyTorch tensors to and from the H5 checkpoint
    """

    @staticmethod
    def save(
        tensor: torch.Tensor, f: h5.File, key: str, **kwargs
    ) -> Type["TorchTensorH5Type"]:
        """Saves the PyTorch tensor to the provided H5 File"""
        from cerebras_pytorch.saver.storage import (
            DeferredTensor,
            lazy_tensor_data_wrapper,
        )

        tensor = lazy_tensor_data_wrapper(tensor)
        if isinstance(tensor, DeferredTensor):
            tensor.save(f, key, **kwargs)
        else:
            tensor = tensor.to("cpu")
            NumpyArrayH5Type.save(cstorch.to_numpy(tensor), f, key, **kwargs)

        return TorchTensorH5Type

    @staticmethod
    def load(f: h5.File, key: str) -> torch.Tensor:
        """Loads the PyTorch tensor from the provided H5 File"""
        from cerebras_pytorch.saver.storage import DeferredH5Tensor

        return DeferredH5Tensor(f.filename, key)
