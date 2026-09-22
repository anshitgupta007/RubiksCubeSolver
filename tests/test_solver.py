
import random

import pytest

from src import cube, solver

SCRAMBLE_MOVES = ["R", "L", "U", "D", "F", "B",
                   "R'", "L'", "U'", "D'", "F'", "B'",
                   "R2", "L2", "U2", "D2", "F2", "B2"]


def make_scrambled_cube(seed, length=20):
    rng = random.Random(seed)
    c = cube.generate()
    scramble = [rng.choice(SCRAMBLE_MOVES) for _ in range(length)]
    for move in scramble:
        cube.apply_moves(c, move)
    return c, scramble


def test_lookup_tables_load_without_error():

    # solve() raises FileNotFoundError/ValueError immediately if a table
    # is missing or empty, rather than hanging -- so just solving the
    # already-solved cube is enough to prove the tables loaded.
    c = cube.generate()
    solution = solver.solve(c)
    assert solution == []


@pytest.mark.parametrize("seed", [1, 2, 3, 4, 5])
def test_solver_returns_cube_to_solved_state(seed):
    c, scramble = make_scrambled_cube(seed)
    solver.solve(c)
    assert c == cube.generate(), (
        f"Solver failed to fully solve scramble: {scramble}"
    )


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_solution_move_count_is_reasonable(seed):
    """
    Thistlethwaite's algorithm is bounded at 45 moves by construction.
    A regression that breaks a stage transition often shows up as an
    unreasonably long "solution" before it shows up as outright failure.
    """
    c, _ = make_scrambled_cube(seed)
    solution = solver.solve(c)
    assert len(solution) <= 45


def test_solution_moves_are_replayable():
    """
    The returned solution list, when replayed against the original
    scrambled state, must independently reproduce the solved cube.
    This catches bugs where solve() mutates the cube correctly but
    returns a solution list that doesn't match what actually happened.
    """
    c, _ = make_scrambled_cube(seed=7)
    c_replay = [face[:] for face in c]  # deep-ish copy of the scrambled state

    solution = solver.solve(c)

    for move in solution:
        cube.apply_moves(c_replay, move)

    assert c_replay == cube.generate()
