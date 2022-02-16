from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from negmas.sao.components.concession import (
    CrispSelfProjectionConcessionEstimator,
    KindConcessionRecommender,
    ProbSelfProjectionConcessionEstimator,
)

from ..components import ConcessionEstimator, ConcessionRecommender
from .modular import MAPNegotiator
from .utilbased import UtilBasedNegotiator

if TYPE_CHECKING:
    from negmas.common import PreferencesChange


__all__ = [
    "TitForTatNegotiator",
    "NaiveTitForTatNegotiator",
    "SimpleTitForTatNegotiator",
]


class TitForTatNegotiator(UtilBasedNegotiator):
    """
    Implements a tit-for-tat strategy.

    Args:
        estimator: A `SAOComponent` that can estimate

    Remarks:
        - This negotiator does not keep an opponent model. It thinks only in terms of changes in its own utility.
          If the opponent's last offer was better for the negotiator compared with the one before it, it considers
          that the opponent has conceded by the difference. This means that it implicitly assumes a zero-sum
          situation.
    """

    def __init__(
        self,
        *args,
        estimator: ConcessionEstimator | None = None,
        offering_recommender: ConcessionRecommender | None = None,
        acceptance_recommender: ConcessionRecommender | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._estimator = (
            estimator
            if estimator is not None
            else ProbSelfProjectionConcessionEstimator()
        )
        self._offering_recommender = (
            offering_recommender
            if offering_recommender is not None
            else KindConcessionRecommender(must_concede=True, inverter=self._inverter)
        )
        self._acceptance_recommender = (
            acceptance_recommender
            if acceptance_recommender is not None
            else self._offering_recommender
        )
        self._pivot_util: float = 1.0
        self._estimator.set_negotiator(self)
        self._offering_recommender.set_negotiator(self)
        self._acceptance_recommender.set_negotiator(self)

    def on_preferences_changed(self, changes: list[PreferencesChange]):
        super().on_preferences_changed(changes)
        self._estimator.on_preferences_changed(changes)

    def respond(self, state, offer):
        self._estimator.before_responding(state, offer)
        return super().respond(state, offer)

    def propose(self, state):
        proposal = super().propose(state)
        if state.step == 0 or not self._estimator.total_concession:
            self._pivot_util = float(self.ufun(proposal))  # type: ignore
        return proposal

    def utility_range_to_accept(self, state) -> tuple[float, float]:
        concession = self._acceptance_recommender(self._estimator(state), state)
        return self._inverter.scale_utilities((self._pivot_util - concession, 1.0))

    def utility_range_to_propose(self, state) -> tuple[float, float]:
        concession = self._offering_recommender(self._estimator(state), state)
        return self._inverter.scale_utilities(
            (self._pivot_util - concession, self._pivot_util)
        )


class NaiveTitForTatNegotiator(TitForTatNegotiator):
    """
    Implements a naive tit-for-tat strategy that does not depend on the availability of an opponent model.

    Args:
        name: Negotiator name
        preferences: negotiator preferences
        ufun: negotiator ufun (overrides preferences)
        parent: A controller
        kindness: How 'kind' is the agent. A value of zero is standard tit-for-tat. Positive values makes the negotiator
                  concede faster and negative values slower.
        stochastic: If `True`, the offers will be randomized above the level determined by the current concession
                        which in turn reflects the opponent's concession.
        punish: If `True` the agent punish a partner who does not seem to conede by requiring higher utilities
        initial_concession: How much should the agent concede in the beginning in terms of utility. Should be a number
                            or the special string value 'min' for minimum concession

    Remarks:
        - This negotiator does not keep an opponent model. It thinks only in terms of changes in its own utility.
          If the opponent's last offer was better for the negotiator compared with the one before it, it considers
          that the opponent has conceded by the difference. This means that it implicitly assumes a zero-sum
          situation.
    """

    def __init__(
        self,
        *args,
        kindness=0.0,
        punish=False,
        initial_concession: float | Literal["min"] = "min",
        total_concession: bool = False,
        rank_only: bool = False,
        stochastic: bool = False,
        **kwargs,
    ):
        estimator = CrispSelfProjectionConcessionEstimator(
            rank_only=rank_only, total_concession=total_concession
        )
        if isinstance(initial_concession, str):
            initial_concession = 0.00
        offering = KindConcessionRecommender(
            initial_concession=initial_concession, kindness=kindness, punish=punish
        )
        acceptance = KindConcessionRecommender(
            initial_concession=initial_concession, kindness=kindness, punish=punish
        )
        super().__init__(
            *args,
            estimator=estimator,
            offering_recommender=offering,
            acceptance_recommender=acceptance,
            stochastic=stochastic,
            **kwargs,
        )
        offering.set_inverter(self._inverter)
        acceptance.set_inverter(self._inverter)


class SimpleTitForTatNegotiator(MAPNegotiator):
    """A simple tit-for-tat negotiator based on the MAP architecture"""
