from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.progress import Progress

console = Console()
APP_NAME = "[bold cyan]ChatNexus[/bold cyan]"


def display_welcome() -> None:
    """Display the branded welcome message with core commands."""
    welcome_art = """
    ███████╗██╗  ██╗ █████╗ ████████╗███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██║     ███████║███████║   ██║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║     ██╔══██║██╔══██║   ██║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ╚██████╗██║  ██║██║  ██║   ██║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    """
    print(Panel.fit(Markdown(welcome_art), style="bold cyan"))
    print(Panel(
        f"""[bold]Welcome to {APP_NAME}![/bold]
[dim]Next-gen AI terminal interface[/dim]

[bold]Commands:[/bold]
  [cyan]/models[/cyan]   List models    [cyan]/download[/cyan] Get new model
  [cyan]/switch[/cyan]   Change model   [cyan]/settings[/cyan] Configure AI
  [cyan]/history[/cyan]  View history   [cyan]/help[/cyan]     Show help
  [cyan]/exit[/cyan]     Quit app""",
        title="Getting Started",
        title_align="left",
        border_style="cyan"
    ))