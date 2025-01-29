from typing import List, Dict, Optional
from difflib import get_close_matches

import ollama
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def get_installed_models() -> List[Dict[str, Optional[str]]]:
    """Retrieve the list of installed models from Ollama."""
    try:
        response = ollama.list()
        models = []
        for model_obj in response.models:
            model_name = getattr(model_obj, 'model', '')
            if not model_name:
                continue
            size = getattr(model_obj, 'size', 0)
            details = getattr(model_obj, 'details', {})
            parameter_size = details.get('parameter_size', '')
            family = details.get('family', '')

            models.append({
                'name': model_name,
                'size': size,
                'parameter_size': parameter_size,
                'family': family
            })
        return models
    except Exception as e:
        console.print(f"[red]Error listing models: {str(e)}[/red]")
        return []


def model_selection() -> Optional[str]:
    """Interactive model selection interface."""
    models = get_installed_models()
    if not models:
        console.print("[yellow]No models installed. Use /download to get started.[/yellow]")
        return None

    console.print("\n[bold]Available Models:[/bold]")
    for idx, model in enumerate(models, 1):
        size_gb = model['size'] / 1e9
        param_info = f" ({model['parameter_size']})" if model['parameter_size'] else ""
        console.print(f"{idx}. [cyan]{model['name']}{param_info}[/cyan] [dim]({size_gb:.1f}GB)[/dim]")

    try:
        choice = Prompt.ask("\nSelect model number", default="1")
        idx = int(choice) - 1
        if 0 <= idx < len(models):
            return models[idx]['name']
        else:
            console.print("[red]Invalid selection[/red]")
            return None
    except ValueError:
        console.print("[red]Please enter a valid number[/red]")
        return None


def download_model(model_name: str) -> Optional[str]:
    """Download a model from Ollama with validation and progress display."""
    from utils import validate_model_name  # Circular import handled

    try:
        model_name = validate_model_name(model_name)
        if not model_name:
            return None

        console.print(f"[dim]Checking model registry for {model_name}...[/dim]")
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Downloading {model_name}...", total=100)

            def progress_hook(data):
                if data.get('status') == 'success':
                    progress.update(task, completed=100)
                elif 'completed' in data and 'total' in data:
                    percentage = (data['completed'] / data['total']) * 100
                    progress.update(task, completed=percentage)

            try:
                ollama.pull(model_name, stream=True, callback=progress_hook)
                console.print(f"[green]✓ Successfully downloaded {model_name}![/green]")
                return model_name
            except ollama.ResponseError as e:
                if 'not found' in str(e).lower():
                    console.print(f"[red]Error: Model '{model_name}' not found in registry[/red]")
                    similar = get_close_matches(model_name, [m['name'] for m in get_installed_models()], n=2)
                    if similar:
                        console.print(f"[dim]Did you mean: {', '.join(similar)}?[/dim]")
                else:
                    console.print(f"[red]Error: {str(e)}[/red]")
                return None

    except Exception as e:
        console.print(f"[red]Download failed: {str(e)}[/red]")
        return None