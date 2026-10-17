"""Command-line entry point: web app by default, terminal mode on request."""

from __future__ import annotations

import argparse
import sys

from rps_arena import __version__
from rps_arena.core import Game, Move

EMOJI = {Move.ROCK: "🪨", Move.PAPER: "📄", Move.SCISSORS: "✂️"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rps-arena", description="Rock, Paper, Scissors.")
    parser.add_argument("--cli", action="store_true", help="play in the terminal instead of the browser")
    parser.add_argument("--port", type=int, default=8080, help="web app port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="don't open a browser tab automatically")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def run_terminal(game: Game | None = None) -> int:
    game = game or Game()
    print("ROCK, PAPER, SCISSORS   (r / p / s, or q to quit)\n")
    try:
        while True:
            raw = input("Your move: ").strip().lower()
            if raw in {"q", "quit", "exit"}:
                break
            try:
                move = Move.parse(raw)
            except ValueError as err:
                print(f"  ✗ {err}\n")
                continue
            result = game.play(move)
            print(f"  You {EMOJI[result.player]}  vs  {EMOJI[result.computer]} Computer  →  {result.outcome.value}")
            print(f"  Score: you {game.player_score} · computer {game.computer_score} · draws {game.draws}\n")
    except (KeyboardInterrupt, EOFError):
        print()
    print(f"Thanks for playing! Final score: you {game.player_score}, computer {game.computer_score}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cli:
        return run_terminal()
    try:
        from rps_arena.web.app import run
    except ImportError:
        print("NiceGUI is not installed, so the web app can't start.\n"
              "Install it with:  pip install nicegui\n"
              "Starting terminal mode instead.\n", file=sys.stderr)
        return run_terminal()
    run(port=args.port, open_browser=not args.no_browser)
    return 0
