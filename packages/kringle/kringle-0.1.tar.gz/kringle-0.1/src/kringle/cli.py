import importlib.util
import os
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any


def _import_solution() -> ModuleType:
    solution_path: Path = Path(os.getcwd()) / "solution.py"
    spec: ModuleSpec = importlib.util.spec_from_file_location("solution", solution_path)  # type: ignore
    solution: ModuleType = importlib.util.module_from_spec(spec)
    sys.modules["solution"] = solution
    spec.loader.exec_module(solution)  # type: ignore

    return solution


def main() -> None:
    """Import the solution and run both parts."""
    solution: ModuleType = _import_solution()

    # Read the challenge data from input.txt and parse it
    with open(Path(os.getcwd()) / "input.txt") as f:
        data: str = f.read()
    parsed_data: Any = solution.parse(data)

    if hasattr(solution, "part_1"):
        print("Part 1: ", solution.part_1(parsed_data))  # noqa: T201
    else:
        print("Part 1: Not yet implemented")  # noqa: T201

    if hasattr(solution, "part_2"):
        print("Part 2: ", solution.part_2(parsed_data))  # noqa: T201
    else:
        print("Part 2: Not yet implemented")  # noqa: T201
