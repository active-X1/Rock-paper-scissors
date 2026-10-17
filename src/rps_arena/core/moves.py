"""Moves and outcomes, plus the rule that decides who wins."""

from __future__ import annotations

from enum import Enum


class Outcome(Enum):
    WIN = "You win!"
    LOSE = "You lose"
    DRAW = "It's a draw"


class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    @property
    def label(self) -> str:
        return self.value.capitalize()

    @property
    def beats(self) -> "Move":
        """The move this one defeats."""
        return {Move.ROCK: Move.SCISSORS, Move.PAPER: Move.ROCK, Move.SCISSORS: Move.PAPER}[self]

    @classmethod
    def parse(cls, text: str) -> "Move":
        """Accept ``rock``/``r``, ``paper``/``p``, ``scissors``/``s`` (any case)."""
        cleaned = text.strip().lower()
        for move in cls:
            if cleaned in {move.value, move.value[0]}:
                return move
        raise ValueError(f"Invalid choice: {text!r}. Use rock, paper or scissors.")


def judge(player: Move, computer: Move) -> Outcome:
    """Return the outcome of a round from the player's point of view."""
    if player is computer:
        return Outcome.DRAW
    return Outcome.WIN if player.beats is computer else Outcome.LOSE
