from typing import List, Dict

from rich.console import Console

from ui import display_welcome
from models import model_selection
from chat import ChatInterface
from constants import APP_NAME  # Import APP_NAME
from exceptions import ValidationError, ModelSelectionError  # Import custom exceptions

console = Console()


def main():
    """Main entry point of the application."""
    history: List[Dict[str, str]] = []
    current_model: Dict[str, str] = {'name': None}

    try:
        display_welcome()
        model_name = model_selection()
        if not model_name:
            console.print(f"[red]No model selected. Exiting...[/red]")
            raise ModelSelectionError("No model selected")
        
        current_model['name'] = model_name
        console.print(f"\n[green]Active Model: {model_name}[/green]")
        chat = ChatInterface(current_model, history)
        chat.chat_loop()

    except ValidationError as ve:
        console.print(f"[red]Validation Error: {str(ve)}[/red]")
    except ModelSelectionError as mse:
        console.print(f"[red]Model Selection Error: {str(mse)}[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Fatal Error: {str(e)}[/red]")
    finally:
        console.print(f"\n{APP_NAME} Session Terminated")


if __name__ == "__main__":
    main()