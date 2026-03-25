from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=BACKEND_ROOT).returncode


def main() -> int:
    targets = ["api", "apps", "core", "runtime", "main.py", "tests"]
    if run(["uv", "run", "ruff", "check", "--fix", *targets]) != 0:
        return 1
    return run(["uv", "run", "ruff", "format", *targets])


if __name__ == "__main__":
    sys.exit(main())
