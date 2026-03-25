from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"


def main() -> int:
    result = subprocess.run(
        [
            "uv",
            "run",
            "xenon",
            "--max-absolute",
            "F",
            "--max-modules",
            "D",
            "--max-average",
            "A",
            "api",
            "apps",
            "core",
            "runtime",
            "main.py",
        ],
        cwd=BACKEND_ROOT,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
