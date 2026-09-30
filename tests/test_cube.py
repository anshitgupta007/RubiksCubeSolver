
import copy
import pytest

from src.rubiks_solver import cube

ALL_MOVES = ["R", "L", "U", "D", "F", "B",
             "R'", "L'", "U'", "D'", "F'", "B'",
             "R2", "L2", "U2", "D2", "F2", "B2"]

QUARTER_TURNS = ["R", "L", "U", "D", "F", "B"]


def solved_cube():
    return cube.generate()


def test_generate_is_solved():
    c = solved_cube()
    # Each face should be a single uniform color (0-5).
    for face_index, face in enumerate(c):
        assert face == [face_index] * 9


@pytest.mark.parametrize("move", QUARTER_TURNS)
def test_quarter_turn_four_times_is_identity(move):
    """Applying the same quarter turn 4 times must return to solved."""
    c = solved_cube()
    for _ in range(4):
        cube.apply_moves(c, move)
    assert c == solved_cube()


@pytest.mark.parametrize("move", QUARTER_TURNS)
def test_double_turn_twice_is_identity(move):
    """Applying a half turn (e.g. R2) twice must return to solved."""
    double = move + "2"
    c = solved_cube()
    cube.apply_moves(c, double)
    cube.apply_moves(c, double)
    assert c == solved_cube()


@pytest.mark.parametrize("move", ALL_MOVES)
def test_move_and_its_inverse_cancel(move):
    """move followed by cube.INVERSE_MOVES[move] must be a no-op."""
    c = solved_cube()
    cube.apply_moves(c, move)
    cube.apply_moves(c, cube.INVERSE_MOVES[move])
    assert c == solved_cube()


@pytest.mark.parametrize("move", ALL_MOVES)
def test_move_preserves_facelet_multiset(move):
    """
    A legal move can only permute facelets, never create/destroy/recolor
    them -- so the count of each of the 6 colors on the whole cube must
    stay 9 each, no matter what move was applied.
    """
    c = solved_cube()
    cube.apply_moves(c, move)
    flat = [sticker for face in c for sticker in face]
    for color in range(6):
        assert flat.count(color) == 9


def test_scramble_and_manual_unscramble_returns_to_solved():
    """
    Apply a fixed scramble, then apply its exact inverse sequence in
    reverse order. This should always return to solved regardless of
    what the scramble was, independent of the solver itself.
    """
    scramble = ["R", "U", "F2", "L'", "D", "B", "R2", "U'", "F", "L2"]
    c = solved_cube()
    for move in scramble:
        cube.apply_moves(c, move)

    for move in reversed(scramble):
        cube.apply_moves(c, cube.INVERSE_MOVES[move])

    assert c == solved_cube()


def test_apply_moves_does_not_mutate_unrelated_faces_incorrectly():
    """
    Regression guard: a bad index in one branch of apply_moves can corrupt
    a face that a given move should never touch. Applying U should never
    change which colors are *possible* on D beyond a legal permutation.
    """
    c = solved_cube()
    before = copy.deepcopy(c)
    cube.apply_moves(c, "U")
    # D face (index 5) is untouched by a U move.
    assert c[5] == before[5]
