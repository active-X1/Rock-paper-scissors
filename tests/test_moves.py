import unittest

from rps_arena.core import Move, Outcome, judge


class MoveTests(unittest.TestCase):
    def test_all_nine_matchups(self):
        expected = {
            (Move.ROCK, Move.ROCK): Outcome.DRAW,
            (Move.ROCK, Move.PAPER): Outcome.LOSE,
            (Move.ROCK, Move.SCISSORS): Outcome.WIN,
            (Move.PAPER, Move.ROCK): Outcome.WIN,
            (Move.PAPER, Move.PAPER): Outcome.DRAW,
            (Move.PAPER, Move.SCISSORS): Outcome.LOSE,
            (Move.SCISSORS, Move.ROCK): Outcome.LOSE,
            (Move.SCISSORS, Move.PAPER): Outcome.WIN,
            (Move.SCISSORS, Move.SCISSORS): Outcome.DRAW,
        }
        for (player, computer), outcome in expected.items():
            with self.subTest(player=player, computer=computer):
                self.assertIs(judge(player, computer), outcome)

    def test_parse_accepts_words_letters_and_case(self):
        self.assertIs(Move.parse("Rock"), Move.ROCK)
        self.assertIs(Move.parse(" p "), Move.PAPER)
        self.assertIs(Move.parse("SCISSORS"), Move.SCISSORS)
        self.assertIs(Move.parse("s"), Move.SCISSORS)

    def test_parse_rejects_garbage(self):
        for bad in ("", "lizard", "rocks", "x"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                Move.parse(bad)


if __name__ == "__main__":
    unittest.main()
