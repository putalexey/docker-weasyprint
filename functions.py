import re

def parse_size_string(size_string):
    """
    Parses a human-readable size string (e.g., "10MB", "2.5GB", "100M") into bytes.
    Handles units like KB, MB, GB, TB (case-insensitive).
    """
    size_string = size_string.strip().upper()  # Normalize input

    # Regular expression to extract number and unit
    match = re.match(r'(\d+\.?\d*)([a-zA-Z]{,2})', size_string)
    if not match:
        raise ValueError("Invalid size string format")

    value = float(match.group(1))
    unit = match.group(2)
    if len(unit) == 0:
        return int(value)

    unit_multipliers = {
        'B': 1,
        'K': 1024,
        'KB': 1024,
        'M': 1024**2,
        'MB': 1024**2,
        'G': 1024**3,
        'GB': 1024**3,
        'T': 1024**4,
        'TB': 1024**4,
    }

    if unit not in unit_multipliers:
        raise ValueError(f"Unknown unit: {unit}")

    return int(value * unit_multipliers[unit])
