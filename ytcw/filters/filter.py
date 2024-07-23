from typing import Any

from ytcw.filters.duplicate_check import duplicate_check


def filter_video(info: dict[str, Any], *, incomplete: bool) -> str | None:
    duplicate_check(info)
    return None
