# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""A power manager implementation that uses the matryoshka algorithm.

When there are multiple proposals from different actors for the same set of batteries,
the matryoshka algorithm will consider the priority of the actors, the bounds they set
and their preferred power to determine the target power for the batteries.

The preferred power of lower priority actors will take precedence as long as they
respect the bounds set by higher priority actors.  If lower priority actors request
power values outside the bounds set by higher priority actors, the target power will
be the closest value to the preferred power that is within the bounds.

When there is only a single proposal for a set of batteries, its preferred power would
be the target power, as long as it falls within the system power bounds for the
batteries.
"""

from __future__ import annotations

import logging
import typing

from typing_extensions import override

from ... import timeseries
from ...timeseries import Power
from . import _bounds
from ._base_classes import BaseAlgorithm, Proposal, Report
from ._sorted_set import SortedSet

if typing.TYPE_CHECKING:
    from ...timeseries.battery_pool import PowerMetrics
    from .. import power_distributing

_logger = logging.getLogger(__name__)


class Matryoshka(BaseAlgorithm):
    """The matryoshka algorithm."""

    def __init__(self) -> None:
        """Create a new instance of the matryoshka algorithm."""
        self._battery_buckets: dict[frozenset[int], SortedSet[Proposal]] = {}
        self._target_power: dict[frozenset[int], Power] = {}

    def _calc_target_power(
        self,
        proposals: SortedSet[Proposal],
        system_bounds: PowerMetrics,
    ) -> Power:
        """Calculate the target power for the given batteries.

        Args:
            proposals: The proposals for the given batteries.
            system_bounds: The system bounds for the batteries in the proposal.

        Returns:
            The new target power for the batteries.
        """
        lower_bound = (
            system_bounds.inclusion_bounds.lower
            if system_bounds.inclusion_bounds
            # if a target power exists from a previous proposal, and the system bounds
            # have become unavailable, force the target power to be zero, by narrowing
            # the bounds to zero.
            else Power.zero()
        )
        upper_bound = (
            system_bounds.inclusion_bounds.upper
            if system_bounds.inclusion_bounds
            else Power.zero()
        )

        exclusion_bounds = None
        if system_bounds.exclusion_bounds is not None and (
            system_bounds.exclusion_bounds.lower != Power.zero()
            or system_bounds.exclusion_bounds.upper != Power.zero()
        ):
            exclusion_bounds = system_bounds.exclusion_bounds

        target_power = Power.zero()
        for next_proposal in reversed(proposals):
            if upper_bound < lower_bound:
                break
            if next_proposal.preferred_power:
                match _bounds.clamp_to_bounds(
                    next_proposal.preferred_power,
                    lower_bound,
                    upper_bound,
                    exclusion_bounds,
                ):
                    case (None, power) | (power, None) if power:
                        target_power = power
                    case (power_low, power_high) if power_low and power_high:
                        if (
                            power_high - next_proposal.preferred_power
                            < next_proposal.preferred_power - power_low
                        ):
                            target_power = power_high
                        else:
                            target_power = power_low

            proposal_lower = next_proposal.bounds.lower or lower_bound
            proposal_upper = next_proposal.bounds.upper or upper_bound
            # If the bounds from the current proposal are fully within the exclusion
            # bounds, then don't use them to narrow the bounds further. This allows
            # subsequent proposals to not be blocked by the current proposal.
            match _bounds.check_exclusion_bounds_overlap(
                proposal_lower, proposal_upper, exclusion_bounds
            ):
                case (True, True):
                    continue
            lower_bound = max(lower_bound, proposal_lower)
            upper_bound = min(upper_bound, proposal_upper)
            lower_bound, upper_bound = _bounds.adjust_exclusion_bounds(
                lower_bound, upper_bound, exclusion_bounds
            )

        return target_power

    def _validate_battery_ids(
        self,
        battery_ids: frozenset[int],
        proposal: Proposal | None,
        system_bounds: PowerMetrics,
    ) -> bool:
        if battery_ids not in self._battery_buckets:
            # if there are no previous proposals and there are no system bounds, then
            # don't calculate a target power and fail the validation.
            if (
                system_bounds.inclusion_bounds is None
                and system_bounds.exclusion_bounds is None
            ):
                if proposal is not None:
                    _logger.warning(
                        "PowerManagingActor: No system bounds available for battery "
                        "IDs %s, but a proposal was given.  The proposal will be "
                        "ignored.",
                        battery_ids,
                    )
                return False

            for bucket in self._battery_buckets:
                if any(battery_id in bucket for battery_id in battery_ids):
                    raise NotImplementedError(
                        f"PowerManagingActor: Battery IDs {battery_ids} are already "
                        "part of another bucket.  Overlapping buckets are not "
                        "yet supported."
                    )
        return True

    @override
    def calculate_target_power(
        self,
        battery_ids: frozenset[int],
        proposal: Proposal | None,
        system_bounds: PowerMetrics,
        must_return_power: bool = False,
    ) -> Power | None:
        """Calculate and return the target power for the given batteries.

        Args:
            battery_ids: The battery IDs to calculate the target power for.
            proposal: If given, the proposal to added to the bucket, before the target
                power is calculated.
            system_bounds: The system bounds for the batteries in the proposal.
            must_return_power: If `True`, the algorithm must return a target power,
                even if it hasn't changed since the last call.

        Returns:
            The new target power for the batteries, or `None` if the target power
                didn't change.

        Raises:  # noqa: DOC502
            NotImplementedError: When the proposal contains battery IDs that are
                already part of another bucket.
        """
        if not self._validate_battery_ids(battery_ids, proposal, system_bounds):
            return None

        if proposal is not None:
            self._battery_buckets.setdefault(battery_ids, SortedSet()).insert(proposal)

        # If there has not been any proposal for the given batteries, don't calculate a
        # target power and just return `None`.
        proposals = self._battery_buckets.get(battery_ids)
        if proposals is None:
            return None

        target_power = self._calc_target_power(proposals, system_bounds)

        if (
            must_return_power
            or battery_ids not in self._target_power
            or self._target_power[battery_ids] != target_power
        ):
            self._target_power[battery_ids] = target_power
            return target_power
        return None

    @override
    def get_status(
        self,
        battery_ids: frozenset[int],
        priority: int,
        system_bounds: PowerMetrics,
        distribution_result: power_distributing.Result | None,
    ) -> Report:
        """Get the bounds for the algorithm.

        Args:
            battery_ids: The IDs of the batteries to get the bounds for.
            priority: The priority of the actor for which the bounds are requested.
            system_bounds: The system bounds for the batteries.
            distribution_result: The result of the last power distribution.

        Returns:
            The target power and the available bounds for the given batteries, for
                the given priority.
        """
        target_power = self._target_power.get(battery_ids)
        if system_bounds.inclusion_bounds is None:
            return Report(
                target_power=target_power,
                _inclusion_bounds=None,
                _exclusion_bounds=system_bounds.exclusion_bounds,
                distribution_result=distribution_result,
            )

        lower_bound = system_bounds.inclusion_bounds.lower
        upper_bound = system_bounds.inclusion_bounds.upper

        exclusion_bounds = None
        if system_bounds.exclusion_bounds is not None and (
            system_bounds.exclusion_bounds.lower != Power.zero()
            or system_bounds.exclusion_bounds.upper != Power.zero()
        ):
            exclusion_bounds = system_bounds.exclusion_bounds

        for next_proposal in reversed(self._battery_buckets.get(battery_ids, [])):
            if next_proposal.priority <= priority:
                break
            proposal_lower = next_proposal.bounds.lower or lower_bound
            proposal_upper = next_proposal.bounds.upper or upper_bound
            match _bounds.check_exclusion_bounds_overlap(
                proposal_lower, proposal_upper, exclusion_bounds
            ):
                case (True, True):
                    continue
            calc_lower_bound = max(lower_bound, proposal_lower)
            calc_upper_bound = min(upper_bound, proposal_upper)
            if calc_lower_bound <= calc_upper_bound:
                lower_bound, upper_bound = _bounds.adjust_exclusion_bounds(
                    calc_lower_bound, calc_upper_bound, exclusion_bounds
                )
            else:
                break
        return Report(
            target_power=target_power,
            _inclusion_bounds=timeseries.Bounds[Power](
                lower=lower_bound, upper=upper_bound
            ),
            _exclusion_bounds=system_bounds.exclusion_bounds,
            distribution_result=distribution_result,
        )
