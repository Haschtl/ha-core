"""Basic helpers."""


def represents_number(s):
    """Check if a variable is convertible to a number."""
    try:
        float(s)
    except ValueError:
        return False
    return True
