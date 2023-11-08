# Copyright 2016-2023 Cerebras Systems
# SPDX-License-Identifier: BSD-3-Clause

import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from inspect import isabstract
from typing import List, Optional

from cerebras_appliance.utils.classes import retrieve_all_subclasses

from .step_closures import step_closure
from .tracker import RateTracker


class Profiler:
    """
    Provides a way to track and query various activities during training.

    Once started, they are accessible as attributes of the profiler object.

    By default, the following activities are tracked:
        - total_samples: the total number of samples processed
        - rate: Smoothed samples/second of all the samples added since last
              queried
        - global_rate: Non-smoothed samples/second since the beginning of when
              the profiler was instantiated
        - total_time: Number of seconds since the profiler was instantiated

    Args:
        outdir: The directory where the performance data will be stored.
        additional_activities: A list of additional activities to track.
    """

    def __init__(
        self,
        outdir: str,
        additional_activities: Optional[List["Activity"]] = None,
    ):
        self.outdir = outdir

        # The assumption is that none of the activities that are tracked by
        # default will cost much to initialize and track. So we initialize and
        # track all of them
        self.activities = {
            name: activity()
            for name, activity in Activity.get_default_activities().items()
        }

        if additional_activities:
            for activity in additional_activities:
                if not isinstance(activity, Activity):
                    raise TypeError(
                        f"Expected an Activity, got {type(activity)}"
                    )

                name = getattr(activity, "name", None)
                if name is None:
                    raise ValueError(
                        f"Activity {activity} does not have a name"
                    )
                elif name in self.activities:
                    raise ValueError(f"Activity {name} already exists")

                self.activities[name] = activity()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.save_perf()
        except Exception as e:
            logging.error(f"Failed to save performance data:\n{e}")
            if exc_type is None:
                # Only raise if there was no exception already
                raise e

    def __getattr__(self, name):
        if name in self.activities:
            return self.activities[name]

        return super().__getattribute__(name)

    def step(self, batch_size):
        """Updates all of the profiler's activities with the given batch size"""
        for activity in self.activities.values():
            activity.update(batch_size)

    def save_perf(self):
        """Saves the performance data to the outdir."""
        perf_data = {
            alias: activity()
            for activity in self.activities.values()
            for alias in activity.aliases
        }
        os.makedirs(self.outdir, exist_ok=True)
        with open(os.path.join(self.outdir, "performance.json"), "w") as f:
            json.dump(perf_data, f, sort_keys=True, indent=4)


@dataclass
class Activity(ABC):
    """
    Defines a single activity that can be profiled

    Args:
        name: The name of the activity. All activities must have a unique name
        track_by_default: If True, this activity will be always be tracked by
            the profiler
        cache: If True, the result of the last compute call will be cached so
            that it can be accessed without recomputing
    """

    name: str
    track_by_default: bool = False

    @abstractmethod
    def update(self, batch_size):
        """Update the current activity with a batch"""

    @abstractmethod
    def compute(self):
        """Compute the current value of this activity"""

    def __call__(self):
        return self.compute()

    def __str__(self):
        return str(self.compute())

    @property
    def aliases(self) -> List[str]:
        """Returns a list of all the aliases of this activity"""
        return [self.name]

    @staticmethod
    def get_default_activities():
        """Returns a list of all available activities"""
        return {
            activity.name: activity
            for activity in retrieve_all_subclasses(Activity)
            if not isabstract(activity) and activity.track_by_default
        }


@dataclass
class RateTrackerActivity(Activity):
    # Its fine for each activity to have its own tracker.
    # They are all initialized virtually at the same time
    # and thus produce the same values
    # The reason each activity has its own tracker is prevent
    # coupling between the profiler and the activities, making
    # it easier for users to define their own activities
    tracker: RateTracker = field(default_factory=RateTracker)
    track_by_default: bool = True

    def __post_init__(self):
        self.reset_time()

    @step_closure
    def reset_time(self):
        """Reset the tracker's start time to the current time"""
        # We reset the tracker's start time inside a step closure here so that
        # the time is reset after compile and execute setup is done.
        # TODO: add an offset of 1 so that the time isn't ~0 when the first
        #       rate/global_rate is computed
        self.tracker.reset_time(offset=0)

    def update(self, batch_size):
        if self.tracker and batch_size:
            self.tracker.add(batch_size)


@dataclass
class TotalSamples(RateTrackerActivity):
    """Returns the total number of samples processed so far"""

    name: str = "total_samples"

    def compute(self):
        return self.tracker.total_count


@dataclass
class TotalTime(RateTrackerActivity):
    """Returns the elapsed time so far"""

    name: str = "total_time"

    def compute(self):
        return self.tracker.elapsed_seconds()


@dataclass
class Rate(RateTrackerActivity):
    """Smoothed samples/second of all the samples added since last queried

    Rate is cached so that it can be accessed without recomputing
    if there were no updates since the last time it was queried
    """

    name: str = "rate"
    cached_result: Optional[float] = None

    def update(self, batch_size):
        super().update(batch_size)
        self.cached_result = None

    def compute(self):
        if self.cached_result is None:
            self.cached_result = self.tracker.rate()
        return self.cached_result


@dataclass
class GlobalRate(RateTrackerActivity):
    """
    Non-smoothed samples/second since the beginning of when the executor
    context was entered

    Global rate is cached so that it can be accessed without recomputing
    if there were no updates since the last time it was queried
    """

    name: str = "global_rate"
    cached_result: Optional[float] = None

    @property
    def aliases(self) -> List[str]:
        return [self.name, "samples_per_sec"]

    def update(self, batch_size):
        super().update(batch_size)
        self.cached_result = None

    def compute(self):
        if self.cached_result is None:
            self.cached_result = self.tracker.global_rate()
        return self.cached_result
