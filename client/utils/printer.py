from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print


def nice_print(title: str, values) -> None:
    console = Console()
    with console.capture() as capture:
        console.print(values)
    str_output = capture.get()
    text = Text.from_ansi(str_output)
    print(Panel(text, title=title, padding=2))
