from typing import Optional
from rich.console import Console
from exceptions import ValidationError  # Import ValidationError
import logging

console = Console()
logger = logging.getLogger(__name__)


def validate_model_name(model_name: str) -> Optional[str]:
    """Sanitize and validate the model name."""
    model_name = model_name.strip().lower()
    if not model_name:
        console.print("[red]Error: Model name cannot be empty[/red]")
        logger.error("Model name cannot be empty.")
        raise ValidationError("Model name cannot be empty")
    if '/' not in model_name:
        console.print("[yellow]⚠ Hint: Use format 'author/modelname' for better results[/yellow]")
        logger.warning("Model name without '/' detected.")
    logger.info(f"Model name validated: {model_name}")
    return model_name