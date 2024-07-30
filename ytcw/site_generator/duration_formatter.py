"""
Includes functions to format the duration in different formats
"""


def duration_to_machine_readable(duration: str) -> str:
    """
    Format the duration string into a machine readable format

    For example 4 hours 18 minutes and 3 seconds (4:18:03): PT4H18M3S

    See: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/time#a_valid_duration_string

    Args:
        duration (str): Duration string

    Returns:
        Returns duration string in machine readable format

    Raises:
        ValueError: If the duration string format is invalid
    """

    parts = list(map(int, duration.split(":")))

    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    elif len(parts) == 1:
        hours = 0
        minutes = 0
        seconds = parts[0]
    else:
        raise ValueError("Invalid duration format")

    label_parts = ["PT"]
    if hours > 0:
        label_parts.append(f"{hours}H")
    if minutes > 0:
        label_parts.append(f"{minutes}M")
    if seconds > 0:
        label_parts.append(f"{seconds}S")

    return "".join(label_parts)
