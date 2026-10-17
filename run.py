"""Convenience launcher: ``python run.py`` (needs ``pip install nicegui`` for the web app)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rps_arena.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
