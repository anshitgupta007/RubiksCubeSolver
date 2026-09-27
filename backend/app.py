"""
Thin FastAPI wrapper around the existing Thistlethwaite solver in src/.
No solving logic lives here -- this only validates input, calls
src.solver.solve() (the same code covered by tests/test_solver.py),
and shapes the response.
"""
import contextlib
import io
import os
import sys
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src import solver  # noqa: E402

app = FastAPI(title="Rubik's Cube Solver API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

VALID_COLORS = set(range(6))


class SolveRequest(BaseModel):
    # 6 faces x 9 stickers, order [Front, Right, Back, Left, Top, Bottom],
    # colors 0-5, matching src/cube.py's exact convention.
    faces: List[List[int]]

    @field_validator("faces")
    @classmethod
    def validate_shape(cls, faces):
        if len(faces) != 6:
            raise ValueError("faces must contain exactly 6 faces")
        for face in faces:
            if len(face) != 9:
                raise ValueError("each face must contain exactly 9 stickers")
            if not all(isinstance(v, int) and v in VALID_COLORS for v in face):
                raise ValueError("sticker colors must be integers 0-5")
        return faces


class SolveResponse(BaseModel):
    solution: List[str]
    move_count: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/solve", response_model=SolveResponse)
def solve_cube(req: SolveRequest):
    state = [face[:] for face in req.faces]

    counts = {}
    for face in state:
        for color in face:
            counts[color] = counts.get(color, 0) + 1
    if any(counts.get(c, 0) != 9 for c in range(6)):
        raise HTTPException(
            status_code=400,
            detail="Invalid cube: each of the 6 colors must appear exactly 9 times.",
        )

    try:

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            solution = solver.solve(state)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Solver error: {exc}")

    return SolveResponse(solution=solution, move_count=len(solution))
