# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

""" The PyTorch/LTC backend implementation """
import contextlib
import inspect
import os
from pathlib import Path
from typing import Dict, Optional, Set, Union

import torch
import torch._lazy  # pylint: disable=import-error

import cerebras_pytorch as cstorch
from cerebras_appliance.log import ClassLogger, named_class_logger
from cerebras_pytorch.amp import init as amp_init
from cerebras_pytorch.amp._amp_state import _amp_state
from cerebras_pytorch.backend.base_backend import (
    COMPILE_ONLY_MSG,
    COMPILE_SUCCESS_MSG,
    PROGRAMMING_CS_MSG,
    BaseBackend,
)
from cerebras_pytorch.core.appliance import ApplianceMode
from cerebras_pytorch.core.configure import _initialize_ltc
from cerebras_pytorch.core.constants import INPUT_NAME_PREFIX, STATE_NAME_PREFIX
from cerebras_pytorch.core.device import LazyDevice
from cerebras_pytorch.core.modes import EVAL
from cerebras_pytorch.lib import cerebras_pytorch_lib
from cerebras_pytorch.saver.checkpoint_reader import CheckpointReader
from cerebras_pytorch.saver.pt_h5_saver import PyTorchH5Saver
from cerebras_pytorch.saver.storage import lazy_tensor_data_wrapper
from cerebras_pytorch.utils.nest import visit_device_tensors


@named_class_logger("LtcBackend")
class PyTorchLtcBackendImpl(BaseBackend, ClassLogger):
    """ The backend subclass for PyTorch/LTC runs """

    def __init__(
        self,
        backend_type,
        artifact_dir: str = None,
        compile_dir: str = None,
        compile_only: bool = False,
        validate_only: bool = False,
        drop_data: bool = False,
        max_checkpoints: Optional[int] = None,
        log_initialization: bool = True,
        use_cs_grad_accum: bool = False,
        micro_batch_size: Optional[int] = None,
        retrace_every_iteration: bool = False,
    ):
        super().__init__(
            backend_type,
            LazyDevice(drop_data=drop_data or compile_only or validate_only),
        )
        if artifact_dir is None:
            self.config.artifact_dir = Path.cwd().joinpath("cerebras_logs")
        else:
            self.config.artifact_dir = Path(artifact_dir)

        self.config.artifact_dir.mkdir(parents=True, exist_ok=True)

        if compile_dir is not None:
            self.config.compile_dir = compile_dir

        self.config.compile_only = compile_only
        self.config.validate_only = validate_only
        self.config.max_checkpoints = max_checkpoints
        self.config.log_initialization = log_initialization
        self.config.use_cs_grad_accum = use_cs_grad_accum
        self.config.micro_batch_size = micro_batch_size

        self.appliance = None

        self.initial_state_file = None

        # To avoid repeated access to the same tensor in appliance we cache
        # all intermediate tensor captured by step closures within compile step
        # inside activations dictionary.
        self.activations: Dict[str, torch.Tensor] = dict()

        self._param_names = set()

        _initialize_ltc(
            verbose=bool(int(os.environ.get("CSTORCH_VERBOSE", "0"))),
            debug=bool(int(os.environ.get("CSTORCH_DEBUG", "1"))),
        )

        # Seed the ltc backend for e.g. dropout. This doesn't influence model
        # initialization or dataloader shuffling.
        if self.seed is not None:
            # pylint: disable=import-error
            cerebras_pytorch_lib.set_rng_state(self.seed)

        self.logger.verbose("Running using LTC backend")

        # Start initialization tracker
        self.appliance_tracker.start("Initialization")

        # Disable retrace every iteration
        self._retrace_every_iteration = retrace_every_iteration
        cerebras_pytorch_lib.retrace_every_iteration(
            self._retrace_every_iteration
        )

    def _generate_tensor_names(
        self, prefix: str, tensors: list, delimiter: str
    ):
        for scope, tensor in visit_device_tensors(
            data_structure=tensors,
            device_type=self.torch_device.type,
            scope=[prefix] if prefix else None,
        ):
            yield delimiter.join(scope), tensor

    def _generate_state_names(self, tensors: list):
        yield from self._generate_tensor_names(
            STATE_NAME_PREFIX, tensors, '.',
        )

    def _generate_input_names(self, tensors: list):
        yield from self._generate_tensor_names(
            INPUT_NAME_PREFIX, tensors, '_',
        )

    def _generate_output_names(self, tensors: list):
        yield from self._generate_tensor_names(
            "output", tensors, '_',
        )

    def mark_output(self, struct, force=False):
        name_mapping = {}
        for name, tensor in self._generate_output_names(struct):
            name_mapping[id(tensor)] = name

        def map_fn(arg):
            if isinstance(arg, torch.Tensor) and (
                arg.device.type == self.torch_device.type
            ):
                name = name_mapping[id(arg)]

                # This might return a new tensor
                # pylint: disable=c-extension-no-member
                return cerebras_pytorch_lib.mark_output_tensor(
                    arg, name=name, force=force
                )

            return arg

        return torch.utils._pytree.tree_map(map_fn, struct)

    ################################################
    #               DataLoader hooks               #
    ################################################

    def on_run_start(self):
        self.appliance_tracker.stop("Initialization")

        super().on_run_start()

        if self.cs_config.precision_opt_level is None:
            self.cs_config.precision_opt_level = 1

        # TODO: only call this if not already initialized
        # initialize automatic mixed precision
        amp_init(verbose=(_amp_state.verbosity == 2),)

        self.logger.verbose(
            f"Appliance total steps:  {self.run_context.num_steps}"
        )
        self.logger.verbose(f"Appliance mode: {self.mode}")

        checkpoint_steps = self.run_context.checkpoint_steps
        if checkpoint_steps is None:
            # TODO: handle case where last checkpoint shouldn't be
            # saved if checkpoint steps was explicitly given to be 0
            # in checkpoint closure
            checkpoint_steps = 0

        self.appliance = ApplianceMode(
            self.config.artifact_dir,
            self.config.compile_dir,
            self.cs_config,
            checkpoint_reader_cls=CheckpointReader,
            use_cs_grad_accum=self.config.use_cs_grad_accum,
            micro_batch_size=self.config.micro_batch_size,
        )

        # pylint: disable=redefined-builtin
        def compile(batch_size: int, cirh_str: str) -> bool:
            self.logger.info(COMPILE_ONLY_MSG)

            with self.appliance.build_worker_image(
                should_skip=self.compile_only or self.validate_only
            ):
                self.appliance.compile(batch_size, cirh_str, self.validate_only)

            self.logger.info(COMPILE_SUCCESS_MSG)
            return True

        def execute(batch_size: int, weights) -> Set[str]:
            if not self.is_e2e_execution:
                return set()

            self.logger.info(PROGRAMMING_CS_MSG)

            if self.mode is None:
                # This means that the user did not call optimizer.step()
                # So, assume that the user wants to run eval
                self.mode = EVAL

                if self.model.training:
                    self.logger.warning(
                        "Model is in training mode but no optimizer.step() "
                        "call was detected. The model will be compiled for "
                        "eval mode but numerics may be affected if ops "
                        "like dropout are present in the model."
                    )

            self.initial_state_file = os.path.join(
                self.device.device_data_dir, f"initial_state.hdf5",
            )

            ini_state_dict = {
                weight.name: lazy_tensor_data_wrapper(weight)
                for weight in weights
            }
            ini_wgt_names = set(ini_state_dict.keys())

            with cstorch.saver.storage.use_external_link(value=True):
                saver = PyTorchH5Saver(max_store=self.config.max_checkpoints)
                saver.save(self.initial_state_file, ini_state_dict)

            # Delete the reference to the weights to release memory (even vms),
            # otherwise OS will fail to allocate enough memory when forking in
            # subsequent calls.
            del ini_state_dict

            self.appliance.execute(
                self.input_fn,
                self.input_fn_params,
                batch_size,
                self.run_context.num_steps,
                checkpoint_steps,
                self.mode,
                self.initial_state_file,
                cleanup_stack=self.run_context.cleanup_stack,
                send_weights_grouper=None,
            )

            # Manually update the skipped weights
            self.appliance.skipped_weights.update(
                self._param_names - ini_wgt_names
            )
            self.logger.debug(
                f"Assigning skipped weights: {self.appliance.skipped_weights}"
            )

            return self.appliance.skipped_weights

        # pylint: disable=c-extension-no-member
        cerebras_pytorch_lib.set_callbacks(
            compile_callback=compile, execute_callback=execute,
        )

        # Call dummy mark_step to trace `detach_copy` ops before actual forward
        # step to avoid difference in LTC graphs between iterations.
        # pylint: disable=protected-access
        torch._lazy.mark_step()

        self.run_step_closures()

        self._param_names = set()

    def on_batch_start(self, batch):
        batch = super().on_batch_start(batch)

        # Clear amp cache for the next iteration
        # pylint: disable=protected-access
        _amp_state.handle._clear_cache()

        def set_tensor_name(tensors: list, names_generator, is_param):
            for name, tensor in names_generator(tensors):
                # pylint: disable=protected-access,c-extension-no-member
                assert cerebras_pytorch_lib.set_parameter_name(tensor, name), (
                    f"failed to set tensor name {name} "
                    f"for tensor: {cerebras_pytorch_lib.get_tensor_info(tensor)}"
                )
                if is_param:
                    self._param_names.add(name)

        set_tensor_name(batch, self._generate_input_names, False)
        set_tensor_name(self.state_dict(), self._generate_state_names, True)

        return batch

    def on_batch_end(self):
        for name, tensor in self._generate_state_names(self.state_dict()):
            if name not in self._param_names:
                continue
            # The following set_alias call also marks the tensor as an output.
            # pylint: disable=protected-access,c-extension-no-member
            assert cerebras_pytorch_lib.set_alias(
                tensor, name
            ), f"failed to set alias {name} for tensor: {cerebras_pytorch_lib.get_tensor_info(tensor)}"

        self._is_tracing = False

        # pylint: disable=protected-access
        if self.retrace_every_iteration or self.run_context.is_initial_step:
            torch._lazy.mark_step()

        self.run_step_closures()

        # Clear activations for the next step
        self.activations.clear()

    @contextlib.contextmanager
    def name_scope(self, name: str):
        # pylint: disable=c-extension-no-member
        old_name = cerebras_pytorch_lib.set_scope_name(name or "")
        yield
        cerebras_pytorch_lib.set_scope_name(old_name)

    def set_name_scope(self, name: str):
        # pylint: disable=c-extension-no-member
        cerebras_pytorch_lib.set_scope_name(name or "")

    ###################################################
    #               Training Loop hooks               #
    ###################################################

    def pre_backward(self, loss):
        """Run just before the call to loss.backward()"""
        if self.grad_scaler is not None:
            self.mark_output({"grad_scalar": self.grad_scaler.state_dict()})
        return loss

    #######################################################
    #               Optimizer related hooks               #
    #######################################################

    def setup_optimizer(self, optimizer):
        super().setup_optimizer(optimizer)
        self.post_optimizer_load_state_dict(optimizer)

    def post_optimizer_load_state_dict(self, optimizer):
        def tensor_cast(value):
            if isinstance(value, torch.Tensor) and value.device.type == "lazy":
                # When we load the optimizer state dict, tensors are moved to
                # device. But we don't want to trace param groups. So we move
                # them back to CPU here.
                value = lazy_tensor_data_wrapper(value).to("cpu")
            elif isinstance(value, int):
                value = torch.tensor(value, dtype=torch.int32)
            elif isinstance(value, float):
                value = torch.tensor(value, dtype=torch.float32)
            elif isinstance(value, (list, tuple)):
                value = type(value)(map(tensor_cast, value))
            return value

        # Convert all python scalars in the param groups to 32 bit torch tensors
        # This is because python int/float are represented as 64-bit scalars,
        # whereas compile can only handle 32-bit scalars.
        for param_group in optimizer.param_groups:
            keys = list(param_group.keys())
            for key in keys:
                if key == "params":
                    continue
                value = param_group.pop(key)
                param_group[key] = tensor_cast(value)

        # Make optimizer state tensors into appliance tensors. When we load a
        # normal torch checkpoint, it's loaded onto CPU. But optimizer state
        # needs to be on the device. Note that loading an optimizer state dict
        # replaces the state variables. This is in constrast to loading a model
        # state dict, which updates the state variables using `param.copy_()`.
        def make_appliance(value):
            if isinstance(value, torch.Tensor) and value.device.type != "lazy":
                return value.to(self.device.torch_device)
            return None

        with self.device:
            optimizer.visit_state(make_appliance)

    def pre_optimizer_step(self, optimizer):
        """Set of actions before the optimizer step has been performed"""
        super().pre_optimizer_step(optimizer)

        # pylint: disable=protected-access
        # Set the lr value to be the tensor
        for lr_scheduler in optimizer._lr_scheduler_registry:
            lr_scheduler.update_last_lr()

    def setup_lr_scheduler(self, lr_scheduler):
        super().setup_lr_scheduler(lr_scheduler)

        lr_scheduler.device = self.torch_device
        with self.device:
            if not isinstance(lr_scheduler.last_epoch, torch.Tensor):
                # The tensor representation of last_epoch
                lr_scheduler.last_epoch = torch.tensor(
                    lr_scheduler.last_epoch, dtype=torch.int64
                )

            lr_scheduler.last_epoch = lr_scheduler.last_epoch.to(
                self.torch_device
            )

    def setup_grad_scaler(self, grad_scaler):
        super().setup_grad_scaler(grad_scaler)

        with self.device:
            state_dict = {
                name: tensor.to(self.torch_device)
                if isinstance(tensor, torch.Tensor)
                else tensor
                for name, tensor in grad_scaler.state_dict().items()
            }
        grad_scaler.load_state_dict(state_dict)

    def _get_cpu_tensor(self, arg: torch.Tensor):
        """Get a CPU tensor from the appliance"""

        # pylint: disable=c-extension-no-member
        name = cerebras_pytorch_lib.get_tensor_name(arg)

        if name not in self.activations:
            if cerebras_pytorch_lib.is_weight_tensor(arg):
                raise RuntimeError(
                    f"Attempting to get weight tensor \"{name}\" with info "
                    f"{cerebras_pytorch_lib.get_tensor_info(arg)} in a step closure "
                    f"but this is not supported yet. Please use "
                    f"\"cstorch.save()\" API to save model weights."
                )
            else:
                tensor = self.appliance.receive_output(
                    self.run_context.iteration, name
                )
                try:
                    # Make the tensor writable so that we don't have to copy it
                    # in `cstorch.from_numpy()`. Some arrays cannot be modified
                    # so we ignore the error and copy the array instead.
                    tensor.flags.writeable = True
                except Exception:  # pylint: disable=broad-except
                    pass

            self.activations[name] = cstorch.from_numpy(tensor)

        return self.activations[name]

    def move_to_device(self, struct):
        if isinstance(struct, torch.nn.Module):

            def _replace_parameters(module: torch.nn.Module):
                parameter_names = [
                    name for name, _ in module.named_parameters(recurse=False)
                ]
                for name in parameter_names:
                    # pylint: disable=protected-access
                    param = module._parameters.pop(name)
                    if not isinstance(param, cstorch.nn.Parameter):
                        # Move tensor data to appliance data if not already there
                        with self.device:
                            ltc_param = param.to(self.torch_device)
                            del param
                            param = cstorch.nn.Parameter(ltc_param)
                    else:
                        param = param.to(self.torch_device)
                    module._parameters[name] = param

            struct.apply(_replace_parameters)

            def _move_buffers(module: torch.nn.Module):
                with self.device:
                    # pylint: disable=protected-access
                    for key, buf in module._buffers.items():
                        if buf is not None:
                            module._buffers[key] = cstorch.nn.Buffer(
                                buf.to(self.torch_device)
                            )

            struct.apply(_move_buffers)

            return struct

        return super().move_to_device(struct)

    def set_attribute(
        self,
        tensor: torch.Tensor,
        attribute: str,
        value: Union[bool, int, float, str],
    ):
        """
        Adds an attribute to the traced tensor at compile time to communicating
        with the Cerebras Compiler Stack.

        Args:
            tensor: A tensor on the backend device.
            attribute: Name of the attribute to set
            value: Value of the attribute to set.
        """

        # These attributes eventally land in MLIR attributes, potentially on
        # the arguments to the main function. MLIR requires such attributes be
        # scoped to a dialect, so ensure the attribute name is prefixed with
        # `cs.`
        name = "cs." + attribute

        from cerebras_pytorch.lib import cerebras_pytorch_lib

        cerebras_pytorch_lib.set_attribute(tensor, name, value)

    #################################################
    #               Appliance related               #
    #################################################

    def add_step_closure(
        self,
        closure,
        args,
        kwargs,
        run_async: bool = False,
        repeat: bool = False,
    ):
        if hasattr(closure, "__wrapped__"):
            pos_arg_names = inspect.getfullargspec(closure.__wrapped__).args
        else:
            pos_arg_names = inspect.getfullargspec(closure).args

        if len(pos_arg_names) == len(args) and not any(
            pos_arg_name in kwargs for pos_arg_name in pos_arg_names
        ):
            # Use the names of the positional arguments in the step closure as
            # the output name.
            kwargs.update(dict(zip(pos_arg_names, args)))
            kwargs = self.mark_output(kwargs, force=True)
            # Strip positional arguments back out
            args = type(args)(
                kwargs.pop(arg_name) for arg_name in pos_arg_names
            )
        else:
            # Use anonymous positional arguments
            args, kwargs = self.mark_output((args, kwargs), force=True)

        self.step_closures.append((closure, args, kwargs, run_async, repeat))

    def run_step_closures(self):
        step_closures = self.step_closures
        self.step_closures = []

        if self.compile_only or self.validate_only:
            self.logger.debug(
                f"Skipping runnning step closures since backend is configured for "
                f"{'compile' if self.compile_only else 'validate'}_only mode."
            )
            return

        # pylint: disable=import-error
        from torch._lazy.closure import AsyncClosureHandler

        async_closure_handler = AsyncClosureHandler()

        for closure, args, kwargs, run_async, repeat in step_closures:
            # fetching tensors from appliance here
            # pylint: disable=protected-access
            cpu_args, cpu_kwargs = torch.utils._pytree.tree_map(
                lambda arg: (
                    self._get_cpu_tensor(arg)
                    if isinstance(arg, torch.Tensor)
                    and arg.device.type == self.torch_device.type
                    else arg
                ),
                (args, kwargs),
            )

            if run_async:
                async_closure_handler.run(
                    lambda c=closure, a=cpu_args, k=cpu_kwargs: c(*a, **k)
                )
            else:
                closure(*cpu_args, **cpu_kwargs)

            if repeat:
                self.step_closures.append(
                    (closure, args, kwargs, run_async, repeat)
                )

    def save(self, state_dict, checkpoint_file):
        saver = PyTorchH5Saver(max_store=self.config.max_checkpoints)
        flattened, spec = saver.flatten_state_dict(state_dict)
        # save the spec before saving tensors so we know what was
        # intended to be saved, even if something fails
        saver.save_spec(checkpoint_file, spec)

        if not self.run_context_stack or self.run_context.is_pre_initial_step:
            # If we are on the first step, we don't need to fetch the
            # tensor from the appliance since it is already the initial
            # tensor value (initial weights).
            # pylint: disable=protected-access,c-extension-no-member
            for key, val in flattened.items():
                if isinstance(val, torch.Tensor):
                    val = lazy_tensor_data_wrapper(val)
                saver.save_tensor(checkpoint_file, key, val)
        else:
            self.appliance.save_weights(
                flattened.items(), checkpoint_file, self.run_context.iteration,
            )

        # Now do some verification that all the tensors in spec were saved
        saved_tensors = PyTorchH5Saver.tensor_names(checkpoint_file)
        missing = set(flattened.keys()) - set(saved_tensors)

        if self.run_context_stack and not self.run_context.is_pre_initial_step:
            # Don't throw an error for known skipped weights
            missing -= set(self.appliance.skipped_weights)

        if missing:
            missing = ', '.join(missing)
            extras = ", ".join(set(saved_tensors) - set(flattened.keys()))
            if extras:
                extra_str = (
                    f"\nUnexpected weights found in checkpoint are: "
                    f"{extras}."
                )
            else:
                extra_str = ""
            raise RuntimeError(
                f"Not all weights from the state dict were saved to the "
                f"checkpoint file `{checkpoint_file}`. This may point to "
                f"an internal error."
                f"\nWeights missing in checkpoint are: {missing}."
                f"{extra_str}"
            )
