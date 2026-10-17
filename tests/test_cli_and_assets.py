import contextlib
import io
import random
import unittest
from pathlib import Path
from unittest import mock

from rps_arena.cli import build_parser, run_terminal
from rps_arena.core import Game, Move

ASSETS = Path(__file__).resolve().parent.parent / "src" / "rps_arena" / "assets"


class TerminalTests(unittest.TestCase):
    def _play(self, inputs):
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(out):
            code = run_terminal(Game(random.Random(0)))
        return code, out.getvalue()

    def test_plays_rounds_and_quits(self):
        code, out = self._play(["r", "p", "q"])
        self.assertEqual(code, 0)
        self.assertEqual(out.count("Score:"), 2)
        self.assertIn("Final score", out)

    def test_invalid_input_is_reported_not_counted(self):
        _, out = self._play(["lizard", "q"])
        self.assertIn("Invalid choice", out)
        self.assertNotIn("Score:", out)

    def test_eof_ends_cleanly(self):
        code, _ = self._play(EOFError())
        self.assertEqual(code, 0)

    def test_parser_defaults(self):
        args = build_parser().parse_args([])
        self.assertEqual((args.cli, args.port, args.no_browser), (False, 8080, False))


class AssetTests(unittest.TestCase):
    def test_every_move_has_artwork(self):
        for move in Move:
            self.assertTrue((ASSETS / f"{move.value}.svg").is_file(), move)

    def test_support_artwork_exists(self):
        for name in ("question.svg", "favicon.svg"):
            self.assertTrue((ASSETS / name).is_file(), name)

    def test_svgs_are_well_formed_xml(self):
        import xml.etree.ElementTree as ET

        for svg in ASSETS.glob("*.svg"):
            with self.subTest(svg=svg.name):
                ET.parse(svg)


if __name__ == "__main__":
    unittest.main()
