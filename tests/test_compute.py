import math
from app import compute_values

def test_compute_values():
    tests = [
        {"name": "positive integer", "input": 4, "square": 16, "root": 2},
        {"name": "zero", "input": 0, "square": 0, "root": 0},
        {"name": "positive float", "input": 2.25, "square": 5.0625, "root": 1.5},
        {"name": "negative integer", "input": -9, "square": 81, "root": None},
        {"name": "large number", "input": 1_000_000, "square": 1_000_000_000_000, "root": 1000},
    ]

    for tc in tests:
        square, root = compute_values(tc["input"])

        assert square == tc["square"], f"{tc['name']}: wrong square"

        if tc["root"] is None:
            assert root is None, f"{tc['name']}: root should be None"
        else:
            assert math.isclose(root, tc["root"], rel_tol=1e-9), f"{tc['name']}: wrong root"
