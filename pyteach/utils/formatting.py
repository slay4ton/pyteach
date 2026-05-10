"""Terminal formatting utilities using rich."""

from rich.console import Console
from rich.panel import Panel
from rich.style import Style

console = Console()


def print_header(text: str, color: str = "cyan"):
    """Print a section header."""
    console.print(Panel(text, style=Style(color=color, bold=True), expand=False))


def print_success(text: str):
    """Print success message."""
    console.print(f"[green]{text}[/green]")


def print_error(text: str):
    """Print error message."""
    console.print(f"[red]{text}[/red]")


def print_info(text: str):
    """Print info message."""
    console.print(f"[yellow]{text}[/yellow]")


def print_code(code: str, language: str = "python"):
    """Print syntax-highlighted code."""
    from rich.syntax import Syntax

    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)
