from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ADR_ROOT = ROOT / "docs" / "adr"
STATUS_VALUES = {
    "Proposed",
    "Accepted",
    "Deprecated",
}
REQUIRED_FIELDS = [
    "Status",
    "Date",
    "Deciders",
    "Supersedes",
    "Superseded by",
]
REQUIRED_SECTIONS = [
    "## Context",
    "## Decision",
    "## Consequences",
    "## Alternatives considered",
    "## Follow-up work",
]
EXPECTED_DECIDER = "avm"
CATEGORY_RULES = {
    "architecture": re.compile(r"^0\d{3}-[a-z0-9-]+\.md$"),
    "product": re.compile(r"^1\d{3}-[a-z0-9-]+\.md$"),
}


def find_links(readme_path: Path) -> list[str]:
    content = readme_path.read_text(encoding="utf-8")
    return re.findall(r"\[\s*([0-9]{4}-[a-z0-9-]+\.md)\s*\]\(\./[^)]+\)", content)


def validate_index(category: str, errors: list[str]) -> None:
    category_dir = ADR_ROOT / category
    readme_path = category_dir / "README.md"
    actual = sorted(path.name for path in category_dir.glob("*.md") if path.name != "README.md")
    indexed = find_links(readme_path)
    if indexed != actual:
        errors.append(
            f"{readme_path.relative_to(ROOT)} index mismatch: indexed={indexed}, actual={actual}"
        )


def validate_file(path: Path, category: str, errors: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    file_name = path.name
    rule = CATEGORY_RULES[category]
    if not rule.match(file_name):
        errors.append(f"{path.relative_to(ROOT)} has invalid filename for category '{category}'")

    number = file_name.split("-", 1)[0]
    title_line = f"# ADR-{number}:"
    if not content.startswith(title_line):
        errors.append(f"{path.relative_to(ROOT)} must start with '{title_line}'")

    for field in REQUIRED_FIELDS:
        if f"- {field}:" not in content:
            errors.append(f"{path.relative_to(ROOT)} missing field '- {field}:'")

    status_match = re.search(r"^- Status:\s*(.+)$", content, flags=re.MULTILINE)
    if not status_match:
        errors.append(f"{path.relative_to(ROOT)} missing status value")
    else:
        status = status_match.group(1).strip()
        if status not in STATUS_VALUES and not status.startswith("Superseded by ADR-"):
            errors.append(f"{path.relative_to(ROOT)} has invalid status '{status}'")

    date_match = re.search(r"^- Date:\s*(\d{4}-\d{2}-\d{2})$", content, flags=re.MULTILINE)
    if not date_match:
        errors.append(f"{path.relative_to(ROOT)} must use Date in YYYY-MM-DD format")

    deciders_match = re.search(r"^- Deciders:\s*(.+)$", content, flags=re.MULTILINE)
    if not deciders_match:
        errors.append(f"{path.relative_to(ROOT)} missing deciders value")
    else:
        deciders = deciders_match.group(1).strip()
        if deciders != EXPECTED_DECIDER:
            errors.append(
                f"{path.relative_to(ROOT)} must use '- Deciders: {EXPECTED_DECIDER}', found '{deciders}'"
            )

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"{path.relative_to(ROOT)} missing section '{section}'")


def main() -> int:
    errors: list[str] = []

    for category in sorted(CATEGORY_RULES):
        validate_index(category, errors)
        category_dir = ADR_ROOT / category
        for path in sorted(category_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            validate_file(path, category, errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("ADR validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
