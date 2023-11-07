from __future__ import annotations  # Not required from python 3.11 onwards
from datetime import datetime
from typing import Any
import csv
from ..observation import Observation
from ..lstindex import LSTInterval, LSTIntervalType


class Observable:
    """
    Represents a valid scheduling time frame based on observational constraints.

    Attributes:
        interval (Any): The time interval or range representing the observation window.
        observation (Any): The observational data or constraints defining the validity of the interval.
    """

    def __init__(self, interval: LSTInterval, observation):
        """
        Initializes an instance of the Observable class.

        :param interval: The time interval or range for the observation window.
        :type interval: Any
        :param observation: The observational constraints or data associated with the interval.
        :type observation: Any
        """
        self._interval = interval
        self._observation = observation

    @property
    def interval(self) -> LSTInterval:
        return self._interval

    @property
    def observation(self) -> Observation:
        return self._observation

    @property
    def id(self) -> Any:
        return self.observation.id

    @property
    def dt(self) -> datetime:
        return self.interval.dt

    @property
    def utc_constraint(self) -> LSTIntervalType:
        return self.interval.type.name

    def __lt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.dt, self.utc_constraint, self.interval.start) < (
            other.dt,
            other.utc_constraint,
            other.interval.start,
        )

    def __le__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.dt, self.utc_constraint, self.interval.start) <= (
            other.dt,
            other.utc_constraint,
            other.interval.start,
        )

    def __eq__(self, __value: Observable) -> bool:
        if not isinstance(__value, type(self)):
            return NotImplemented
        return (
            self.interval.dt,
            self.utc_constraint,
            self.interval.start,
            self.interval.end,
            self.observation.id,
        ) == (
            __value.interval.dt,
            __value.utc_constraint,
            __value.interval.start,
            __value.interval.end,
            __value.observation.id,
        )

    def __ge__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.dt, self.utc_constraint, self.interval.start) >= (
            other.dt,
            other.utc_constraint,
            other.interval.start,
        )

    def __gt__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.dt, self.utc_constraint, self.interval.start) > (
            other.dt,
            other.utc_constraint,
            other.interval.start,
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.interval.dt,
                self.utc_constraint,
                self.interval.start,
                self.interval.end,
                self.observation.id,
            )
        )

    def __str__(self) -> int:
        return f"{self.interval.dt}{self.interval.type}{self.interval.start}{self.interval.end}{self.observation.id}"

    def to_tuple(self):
        return (
            self.id,
            self.dt.strftime("%Y-%m-%d"),
            self.utc_constraint,
            round(self.interval.start, 2),
            round(self.interval.end, 2),
        )
