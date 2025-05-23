from rich.console import Console
from rich.markdown import Markdown

def print(text: str):
    """Print the given text"""
    console = Console()
    console.print(Markdown(text))

