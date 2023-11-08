# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

"""The executor used to configure the run"""
import os
from contextlib import ExitStack
from threading import Event
from typing import List, Optional

from cerebras_appliance.CSConfig import CSConfig
from cerebras_appliance.log import ClassLogger, named_class_logger
from cerebras_pytorch.backend import current_backend_impl
from cerebras_pytorch.utils.tensorboard import SummaryWriter

from ..profiler import Activity, Profiler
from .dataloader import DataLoader


@named_class_logger
class DataExecutor(ClassLogger):
    """Defines a single execution run on a Cerebras wafer scale cluster"""

    # pylint: disable=super-init-not-called
    def __init__(
        self,
        dataloader: DataLoader,
        num_steps: Optional[int] = None,
        checkpoint_steps: Optional[int] = None,
        cs_config: Optional[CSConfig] = None,
        writer: Optional[SummaryWriter] = None,
        additional_activities: Optional[List[Activity]] = None,
    ):
        """
        Args:
            dataloader: the dataloader to use for the run
            num_steps: the number of steps to run. Defaults to 1 if the backend
                was configured for compile or validate only
            checkpoint_steps: the interval at which to schedule fetching
                checkpoints from the cluster
            cs_config: optionally, a
                :py:class:`~cerebras_pytorch.utils.CSConfig` object can be passed
                in to configure the cerebras wafer-scale cluster. if none provided
                the default configuration values will be used.
            writer: The summary writer to be used to write any summarized
                scalars or tensors to tensorboard
            additional_activities: The list of additional activities to profile.
                By default the total samples, the client side rate and global
                rate are tracked and accessible via the profiler attribute
        """
        self.dataloader = dataloader

        self.backend = current_backend_impl()

        if not self.backend.is_e2e_execution:
            if num_steps and num_steps > 1:
                self.logger.warning(
                    "Specified num_steps > 1 when backend was configured "
                    "for compile/validate only. Setting num_steps to 1."
                )
            num_steps = 1
        elif num_steps is None or num_steps < 1:
            raise RuntimeError(f"Expected num_steps >= 1, but got {num_steps}.")

        if cs_config and not isinstance(cs_config, CSConfig):
            raise TypeError(
                f"Expected cs_config to be a CSConfig object. "
                f"Got: {type(cs_config)}"
            )

        if writer is not None and not isinstance(writer, SummaryWriter):
            raise TypeError(
                f"Expected writer to be a "
                f"cstorch.utils.tensorboard.SummaryWriter object. "
                f"Got: {type(writer)}"
            )

        # Disable DL state capture if checkpoint_steps is 0 or None
        if not checkpoint_steps:
            self.dataloader.disable_dataloader_checkpointing()

        self.run_context = RunContext(
            dataloader,
            num_steps,
            checkpoint_steps,
            cs_config,
            writer,
            additional_activities,
        )

    @property
    def profiler(self):
        """Returns the executor profiler"""
        if self._profiler is None:
            raise RuntimeError(
                "Cannot access the profiler in compile/validation modes"
            )
        return self._profiler

    def __len__(self):
        return len(self.run_context)

    @property
    def iteration(self):
        """Returns the current step that the executor is on"""
        return self.run_context.iteration

    @property
    def on_final_iteration(self):
        """Returns whether the executor is on the final step"""
        return self.run_context.is_final_step

    @property
    def profiler(self):
        return self.run_context.profiler

    def __enter__(self):
        self.backend.serialize_input_fn(
            self.dataloader.input_fn, self.dataloader.input_fn_params
        )

        self.run_context.__enter__()

        # Load DL state for data checkpointing
        self.dataloader.serialize_state_dict()

        # Communicate DL checkpointing status to appliance
        if self.backend.backend_type.is_csx:
            self.backend.appliance.enable_dataloader_checkpointing = (
                self.dataloader.enable_dataloader_checkpointing
            )

    def __exit__(self, *args):
        self.run_context.__exit__(*args)

    def __iter__(self):
        with self:

            def get_batches():
                while True:
                    iterable = iter(self.dataloader)
                    try:
                        batch = next(iterable)
                    except StopIteration:
                        raise RuntimeError(
                            "Iterating the dataloader did not return any values. "
                            "This is possibly because the dataset is too small "
                            "for the specified batch_size or drop_last settings. "
                            "Please make sure that the dataloader is able to generate "
                            "at least one batch."
                        )

                    yield batch

                    if self.backend.backend_type.is_csx:
                        while True:
                            yield batch

                    try:
                        while True:
                            yield next(iterable)
                    except StopIteration:
                        # If the iterable is exhausted, we need to start again
                        pass

            for _step, batch in zip(self.run_context, get_batches()):
                yield self.backend.on_batch_start(batch)

                if self.profiler is not None:
                    # Update the profiler as we have processed a batch
                    self.profiler.step(self.dataloader.batch_size)

                self.backend.on_batch_end()


class RunContext:
    """Defines a single run of the appliance"""

    def __init__(
        self,
        dataloader: DataLoader,
        num_steps: Optional[int] = None,
        checkpoint_steps: Optional[int] = None,
        cs_config: Optional[CSConfig] = None,
        writer: Optional[SummaryWriter] = None,
        additional_activities: Optional[List[Activity]] = None,
    ):
        self.backend = current_backend_impl()

        if not isinstance(dataloader, DataLoader):
            raise TypeError(
                "Detected that dataloader was not wrapped using a "
                "cstorch.utils.data.DataLoader.\n"
                "Please wrap your dataloader in a Cerebras Dataloader:\n\n"
                "\tdataloader = cstorch.utils.data.DataLoader(input_fn, ...)\n\n"
                "where `input_fn` is a callable that returns a PyTorch dataloader. "
                "For more details, please see the documentation for "
                "cstorch.utils.data.DataLoader."
            )

        self.dataloader = dataloader
        self.num_steps = num_steps
        self.checkpoint_steps = checkpoint_steps

        # Event that keeps track of whether tracing has occurred
        self.traced = Event()

        self.cs_config = cs_config if cs_config else CSConfig()

        self.writer = writer

        self.step = -1
        self.cleanup_stack = None

        self.profiler = None
        self.additional_activities = additional_activities

    @property
    def is_pre_initial_step(self):
        """Returns true if the current step less than zero"""
        return self.step < 0

    @property
    def is_initial_step(self):
        """Returns true if the current step is zero"""
        return self.step == 0

    @property
    def is_final_step(self):
        """Returns true if the current step is the final step"""
        return self.step + 1 >= self.num_steps

    @property
    def is_checkpoint_step(self):
        """Returns true if the current step is a checkpoint step"""
        step = self.step + 1
        return (step % self.checkpoint_steps == 0) or step == self.num_steps

    @property
    def iteration(self):
        """Returns current step"""
        return self.step

    def __len__(self):
        return self.num_steps

    def __enter__(self):
        self.backend.run_context_stack.append(self)
        self.step = -1  # set step < 0 before the run starts
        self.backend.on_run_start()
        self.step = 0  # set step to 0 as we enter the context
        self.cleanup_stack = ExitStack()
        self.cleanup_stack.__enter__()

        if self.backend.is_e2e_execution:
            self.profiler = Profiler(
                outdir=os.path.join(
                    self.backend.config.artifact_dir, "performance"
                ),
                additional_activities=self.additional_activities,
            )
            self.profiler.__enter__()

    def __exit__(self, *args):
        ctx = self.backend.run_context_stack.pop()
        assert ctx is self
        self.cleanup_stack.__exit__(*args)
        self.backend.on_run_end()
        self.cleanup_stack = None

        if self.profiler is not None:
            self.profiler.__exit__(*args)

    def __iter__(self):
        # sanity check as the user should never use RunContext directly
        assert self.cleanup_stack is not None

        while self.step < self.num_steps:
            yield self.step
            self.step += 1

            if self.backend.retrace_every_iteration:
                self.traced.clear()
