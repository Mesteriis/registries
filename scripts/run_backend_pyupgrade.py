from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"


def main() -> int:
    include_roots = [
        BACKEND_ROOT / "api",
        BACKEND_ROOT / "apps",
        BACKEND_ROOT / "core",
        BACKEND_ROOT / "runtime",
        BACKEND_ROOT / "tests",
    ]
    files = sorted(
        str(path.relative_to(BACKEND_ROOT))
        for root in include_roots
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
    )
    files.append("main.py")
    if not files:
        print("No backend Python files found.")
        return 0

    result = subprocess.run(["uv", "run", "pyupgrade", "--py314-plus", *files], cwd=BACKEND_ROOT)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
