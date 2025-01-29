from typing import Optional
from rich.console import Console

console = Console()


def validate_model_name(model_name: str) -> Optional[str]:
    """Sanitize and validate the model name."""
    model_name = model_name.strip().lower()
    if not model_name:
        console.print("[red]Error: Model name cannot be empty[/red]")
        return None
    if '/' not in model_name:
        console.print("[yellow]⚠ Hint: Use format 'author/modelname' for better results[/yellow]")
    return model_name