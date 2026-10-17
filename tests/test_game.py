import random
import unittest

from rps_arena.core import Game, Move, Outcome


class GameTests(unittest.TestCase):
    def test_scores_and_draws(self):
        game = Game()
        game.play(Move.ROCK, Move.SCISSORS)   # win
        game.play(Move.ROCK, Move.PAPER)      # lose
        game.play(Move.ROCK, Move.ROCK)       # draw
        self.assertEqual((game.player_score, game.computer_score, game.draws), (1, 1, 1))
        self.assertEqual(game.rounds_played, 3)

    def test_streaks(self):
        game = Game()
        for _ in range(3):
            game.play(Move.PAPER, Move.ROCK)
        self.assertEqual((game.streak, game.best_streak), (3, 3))
        game.play(Move.PAPER, Move.SCISSORS)  # loss breaks the streak
        self.assertEqual((game.streak, game.best_streak), (0, 3))

    def test_draw_keeps_streak(self):
        game = Game()
        game.play(Move.PAPER, Move.ROCK)
        game.play(Move.PAPER, Move.PAPER)
        self.assertEqual(game.streak, 1)

    def test_reset(self):
        game = Game()
        game.play(Move.ROCK, Move.SCISSORS)
        game.reset()
        self.assertEqual((game.rounds_played, game.streak, game.best_streak, game.history), (0, 0, 0, []))

    def test_history_is_capped_and_recent_is_newest_last(self):
        game = Game()
        for _ in range(Game.HISTORY_LIMIT + 20):
            game.play(Move.ROCK, Move.ROCK)
        game.play(Move.ROCK, Move.SCISSORS)
        self.assertEqual(len(game.history), Game.HISTORY_LIMIT)
        self.assertIs(game.recent(3)[-1].outcome, Outcome.WIN)

    def test_seeded_computer_is_reproducible(self):
        a, b = Game(random.Random(42)), Game(random.Random(42))
        self.assertEqual([a.pick_computer_move() for _ in range(10)],
                         [b.pick_computer_move() for _ in range(10)])

    def test_computer_uses_every_move(self):
        game = Game(random.Random(1))
        self.assertEqual({game.pick_computer_move() for _ in range(200)}, set(Move))


if __name__ == "__main__":
    unittest.main()
