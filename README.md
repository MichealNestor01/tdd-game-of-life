# TDD Game Of Life Kata

Started this at the software crafters meetup on 23rd Jan 2025, with [AbbyAdj](https://github.com/AbbyAdj), [FunkeGoodVibe](https://github.com/FunkeGoodVibe) and [nneil](https://github.com/nneil).

This is a soltution to the [Conway's Game of Life Kata](https://www.codurance.com/katas/conways-game-of-life). The `GameBoard` class should probably have some tests, but we were focused on the rules of the game. The idea is that various interfaces for the game in future could use this class and the `perform_game_step_iteration` and not have ot worry about the implementation of the game.

## Running the code

To run the code do this:

```
python src/addition.py
```

To run the tests do this:

```
python -m unittest tests.addition_test
```
