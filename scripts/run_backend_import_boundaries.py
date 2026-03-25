from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"


def main() -> int:
    result = subprocess.run(["uv", "run", "lint-imports"], cwd=BACKEND_ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
