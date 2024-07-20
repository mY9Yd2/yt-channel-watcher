from typing import Any

from filters.already_exists import already_exists


def filter_video(info: dict[str, Any], *, incomplete: bool) -> str | None:
    already_exists(info)
    return None
