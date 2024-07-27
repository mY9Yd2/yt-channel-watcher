def duration_to_machine_readable(duration: str):
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
