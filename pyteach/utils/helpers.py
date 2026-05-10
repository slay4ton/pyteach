"""Helper utilities."""

from typing import List, Tuple


def parse_user_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse user input into command and args."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def format_code_snippet(code: str, max_lines: int = 10) -> str:
    """Format a code snippet for display."""
    lines = code.split("\n")
    if len(lines) > max_lines:
        return "\n".join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines)"
    return code
