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
            "tryceratops",
            "-i",
            "TRY003",
            "-i",
            "TRY300",
            "-i",
            "TRY301",
            "-i",
            "TRY101",
            "-i",
            "TRY203",
            "-i",
            "TRY401",
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
