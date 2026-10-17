"""Game state: scores, streaks and round history."""

from __future__ import annotations

import random
from dataclasses import dataclass

from rps_arena.core.moves import Move, Outcome, judge


@dataclass(frozen=True)
class Round:
    """The result of one played round."""

    player: Move
    computer: Move
    outcome: Outcome


class Game:
    """Tracks a session of rounds against a random computer opponent."""

    HISTORY_LIMIT = 100

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()
        self.reset()

    def reset(self) -> None:
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        self.streak = 0
        self.best_streak = 0
        self.history: list[Round] = []

    @property
    def rounds_played(self) -> int:
        return self.player_score + self.computer_score + self.draws

    def pick_computer_move(self) -> Move:
        return self._rng.choice(list(Move))

    def play(self, player: Move, computer: Move | None = None) -> Round:
        """Play one round. ``computer`` may be forced (useful in tests)."""
        computer = computer or self.pick_computer_move()
        outcome = judge(player, computer)

        if outcome is Outcome.WIN:
            self.player_score += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
        elif outcome is Outcome.LOSE:
            self.computer_score += 1
            self.streak = 0
        else:
            self.draws += 1

        result = Round(player, computer, outcome)
        self.history.append(result)
        del self.history[: -self.HISTORY_LIMIT]
        return result

    def recent(self, count: int = 8) -> list[Round]:
        """The latest rounds, newest last."""
        return self.history[-count:]
