import re

def sanitize_filename(name: str) -> str:
    """Removes illegal characters from a filename."""
    return re.sub(r'[\\/*?:"<>|]', "", name)
