"""NiceGUI front end. Each browser tab gets its own game session."""

from __future__ import annotations

import asyncio
from pathlib import Path

from nicegui import app, ui

from rps_arena import __version__
from rps_arena.core import Game, Move, Outcome, Round
from rps_arena.web.styles import CSS

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
ASSET_URL = "/rps-assets"
REVEAL_DELAY = 0.7  # seconds of suspense before the computer's move is shown

OUTCOME_CLASS = {Outcome.WIN: "win", Outcome.LOSE: "lose", Outcome.DRAW: "draw"}
KEYS = {Move.ROCK: "R", Move.PAPER: "P", Move.SCISSORS: "S"}


def icon_url(move: Move | None) -> str:
    """URL of the artwork for a move (``None`` gives the hidden-move '?')."""
    return f"{ASSET_URL}/{move.value if move else 'question'}.svg"


class ArenaPage:
    """Builds the page and handles interaction for one browser session."""

    def __init__(self, game: Game | None = None) -> None:
        self.game = game or Game()
        self.busy = False
        self.chosen: Move | None = None      # the player's pending pick
        self.last: Round | None = None       # the most recent finished round

        self.scoreboard = ui.refreshable(self._render_scoreboard)
        self.arena = ui.refreshable(self._render_arena)
        self.trail = ui.refreshable(self._render_trail)
        self._build()

    # ------------------------------------------------------------------ layout
    def _build(self) -> None:
        ui.dark_mode(True)
        with ui.element("div").classes("rps-shell"):
            with ui.element("div").classes("rps-header"):
                ui.label("Rock · Paper · Scissors").classes("rps-title")
                ui.label("Beat the computer. Press R, P or S, or tap a card.").classes("rps-sub")

            self.scoreboard()
            self.arena()

            with ui.element("div").classes("rps-picks"):
                for move in Move:
                    self._pick_button(move)

            with ui.element("div").classes("rps-meta"):
                self.trail()
                reset = ui.element("button").classes("rps-reset").props('type="button"')
                reset.on("click", self.reset)
                with reset:
                    ui.label("Reset scores")

            ui.label(f"RPS Arena v{__version__} · built with Python & NiceGUI").classes("rps-footer")

        # Keep shortcuts alive after a card (a <button>) has been clicked.
        ui.keyboard(on_key=self._on_key, repeating=False, ignore=["input", "select", "textarea"])

    def _pick_button(self, move: Move) -> None:
        button = ui.element("button").classes(f"rps-pick glass {move.value}").props('type="button"')
        button.on("click", lambda _e, m=move: self.pick(m))
        with button:
            ui.element("img").props(f'src="{icon_url(move)}" alt="{move.label}"')
            ui.label(move.label).classes("name")
            ui.label(f"press {KEYS[move]}").classes("key")

    # --------------------------------------------------------------- renderers
    def _render_scoreboard(self) -> None:
        g = self.game
        with ui.element("div").classes("rps-scoreboard"):
            for css, value, caption in (
                ("you", g.player_score, "You"),
                ("tie", g.draws, "Draws"),
                ("cpu", g.computer_score, "Computer"),
            ):
                with ui.element("div").classes(f"rps-score glass {css}"):
                    ui.label(str(value)).classes("num")
                    ui.label(caption).classes("cap")

    def _render_arena(self) -> None:
        shown_player = self.last.player if self.last and self.chosen is None else self.chosen
        revealed = self.last is not None and self.chosen is None
        shown_computer = self.last.computer if revealed else None

        with ui.element("div").classes("rps-arena glass"):
            self._panel("You", shown_player, pop=shown_player is not None,
                        caption=shown_player.label if shown_player else "Your move?")
            ui.label("VS").classes("rps-vs")
            thinking = self.chosen is not None
            self._panel("Computer", shown_computer, pop=revealed, shake=thinking,
                        caption=shown_computer.label if shown_computer else ("Thinking…" if thinking else "Waiting"))

        if revealed:
            text = self.last.outcome.value
            ui.label(text).classes(f"rps-banner {OUTCOME_CLASS[self.last.outcome]}")
        else:
            ui.label("Thinking…" if self.chosen else "Make your move").classes("rps-banner wait")

    def _panel(self, who: str, move: Move | None, *, pop: bool = False, shake: bool = False, caption: str = "") -> None:
        with ui.element("div").classes("rps-panel"):
            ui.label(who).classes("who")
            state = "shake" if shake else "pop" if pop else "idle"
            ui.element("img").classes(f"rps-icon {state}").props(
                f'src="{icon_url(move)}" alt="{move.label if move else "Hidden move"}"'
            )
            ui.label(caption).classes("what")

    def _render_trail(self) -> None:
        recent = self.game.recent(8)
        with ui.element("div").classes("rps-trail"):
            if not recent:
                ui.label("No rounds yet")
                return
            for rnd in recent:
                ui.element("div").classes(f"rps-dot {OUTCOME_CLASS[rnd.outcome]}").props(
                    f'title="{rnd.player.label} vs {rnd.computer.label}"'
                )
            streak = self.game.streak
            best = self.game.best_streak
            ui.label(f"Streak {streak} · Best {best}").style("margin-left:10px")

    # ----------------------------------------------------------------- actions
    async def pick(self, move: Move) -> None:
        if self.busy:
            return
        self.busy = True
        self.chosen = move
        self.arena.refresh()
        try:
            await asyncio.sleep(REVEAL_DELAY)
            self.last = self.game.play(move)
        finally:
            self.chosen = None
            self.busy = False
        self.arena.refresh()
        self.scoreboard.refresh()
        self.trail.refresh()

    def reset(self, _event=None) -> None:
        if self.busy:
            return
        self.game.reset()
        self.chosen = None
        self.last = None
        self.arena.refresh()
        self.scoreboard.refresh()
        self.trail.refresh()

    async def _on_key(self, event) -> None:
        action = getattr(event, "action", None)
        if action is not None and not getattr(action, "keydown", True):
            return
        modifiers = getattr(event, "modifiers", None)
        if getattr(modifiers, "ctrl", False) or getattr(modifiers, "meta", False) or getattr(modifiers, "alt", False):
            return  # leave browser shortcuts such as Ctrl+R alone
        name = str(getattr(getattr(event, "key", None), "name", "")).lower()
        for move in Move:
            if name == KEYS[move].lower():
                await self.pick(move)
                return


@ui.page("/")
def index() -> None:
    ui.add_css(CSS)
    ArenaPage()


def run(port: int = 8080, open_browser: bool = True) -> None:
    """Start the web server."""
    app.add_static_files(ASSET_URL, ASSETS_DIR)
    ui.run(
        title="RPS Arena",
        favicon=str(ASSETS_DIR / "favicon.svg"),
        port=port,
        show=open_browser,
        reload=False,
        dark=True,
    )
