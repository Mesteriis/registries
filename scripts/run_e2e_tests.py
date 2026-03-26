from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    result = subprocess.run(
        ["uv", "run", "--project", "src/backend", "pytest", "-x", "-q", "tests/e2e"],
        cwd=ROOT,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
