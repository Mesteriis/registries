from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"


def main() -> int:
    targets = ["api", "apps", "core", "runtime", "main.py", "tests"]
    check = subprocess.run(["uv", "run", "ruff", "check", *targets], cwd=BACKEND_ROOT)
    if check.returncode != 0:
        return check.returncode

    format_check = subprocess.run(
        ["uv", "run", "ruff", "format", "--check", *targets],
        cwd=BACKEND_ROOT,
    )
    return format_check.returncode


if __name__ == "__main__":
    sys.exit(main())
