from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FRONTEND_ROOT = ROOT / "src" / "frontend"


def main() -> int:
    result = subprocess.run(["pnpm", "type-check"], cwd=FRONTEND_ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
