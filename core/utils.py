import re
from typing import Optional


def normalize_username(value: Optional[str]) -> str:
    """Collapse whitespace and strip unwanted characters for username fields."""

    if value is None:
        return ""

    if not isinstance(value, str):
        value = str(value)

    # Remove leading/trailing whitespace and collapse internal spaces.
    cleaned = re.sub(r"\s+", "", value.strip())
    return cleaned
