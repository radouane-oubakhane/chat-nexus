import sys
from typing import List, Dict
from difflib import get_close_matches

from rich.console import Console
from rich.prompt import Prompt, Confirm

from models import get_installed_models, download_model, model_selection
from ui import display_welcome
from chat import ChatInterface
from utils import validate_model_name
from constants import APP_NAME  # Import APP_NAME

COMMAND_LIST = ['/models', '/download', '/switch', '/settings', '/history', '/exit', '/help']
console = Console()


def handle_command(command: str, history: List[Dict[str, str]], current_model: Dict[str, str]) -> bool:
    """
    Handle user commands.

    Returns True if the loop should continue, False otherwise.
    """
    cmd_parts = command.split()
    base_cmd = cmd_parts[0].lower() if cmd_parts else command

    if not base_cmd:
        return True

    if base_cmd not in COMMAND_LIST:
        matches = get_close_matches(base_cmd, COMMAND_LIST, n=2, cutoff=0.6)
        if matches:
            suggestion = " or ".join(matches)
            console.print(f"[yellow]⚠[/yellow] [red]Unknown command:[/red] {base_cmd} Did you mean [cyan]{suggestion}[/cyan]?")
        else:
            console.print(f"[yellow]⚠[/yellow] [red]Unknown command:[/red] {base_cmd}")
        return True

    try:
        if base_cmd == '/exit':
            console.print(f"[bold]{APP_NAME} Sessions Ended[/bold]")
            sys.exit(0)

        elif base_cmd == '/models':
            models = get_installed_models()
            if models:
                console.print("\n[bold]Installed Models:[/bold]")
                for model in models:
                    size_gb = model['size'] / 1e9
                    console.print(f"  - [cyan]{model['name']}[/cyan] [dim]({size_gb:.1f}GB)[/dim]")
            else:
                console.print("[dim]No models installed.[/dim]")

        elif base_cmd == '/download':
            model_name = ' '.join(cmd_parts[1:]) if len(cmd_parts) > 1 else Prompt.ask("Enter model name to download")
            if model_name:
                downloaded_model = download_model(model_name)
                if downloaded_model:
                    current_model['name'] = downloaded_model
                    console.print(f"[green]✓ Successfully downloaded and set as current model: [bold]{downloaded_model}[/bold][/green]")

        elif base_cmd == '/switch':
            new_model = model_selection()
            if new_model:
                current_model['name'] = new_model
                console.print(f"[green]✓ Switched to model: [bold]{new_model}[/bold][/green]")

        elif base_cmd == '/history':
            if not history:
                console.print("[dim]No conversation history yet[/dim]")
                return True
            console.print("\n[bold]Conversation History:[/bold]")
            for idx, msg in enumerate(history, 1):
                role = "You" if msg['role'] == 'user' else "AI"
                console.print(f"[dim]#{idx}[/dim] [bold]{role}:[/bold] {msg['content']}")

        elif base_cmd == '/settings':
            console.print("[bold]Feature Coming Soon![/bold]")
            console.print("[dim]Upcoming settings: temperature, max tokens, system prompts[/dim]")

        elif base_cmd == '/help':
            display_welcome()

    except Exception as e:
        console.print(f"[red]Command Error: {str(e)}[/red]")

    return True