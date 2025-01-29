import logging
from typing import List, Dict

from rich.console import Console

from ui import display_welcome
from models import model_selection
from chat import ChatInterface
from constants import APP_NAME  # Import APP_NAME
from exceptions import ValidationError, ModelSelectionError  # Import custom exceptions

console = Console()

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point of the application."""
    history: List[Dict[str, str]] = []
    current_model: Dict[str, str] = {'name': None}

    try:
        display_welcome()
        logger.info("Displayed welcome message.")
        model_name = model_selection()
        logger.info(f"Model selected: {model_name}")
        if not model_name:
            console.print(f"[red]No model selected. Exiting...[/red]")
            logger.error("No model selected.")
            raise ModelSelectionError("No model selected")
        
        current_model['name'] = model_name
        console.print(f"\n[green]Active Model: {model_name}[/green]")
        logger.info(f"Active Model set to: {model_name}")
        chat = ChatInterface(current_model, history)
        chat.chat_loop()

    except ValidationError as ve:
        console.print(f"[red]Validation Error: {str(ve)}[/red]")
        logger.error(f"Validation Error: {ve}")
    except ModelSelectionError as mse:
        console.print(f"[red]Model Selection Error: {str(mse)}[/red]")
        logger.error(f"Model Selection Error: {mse}")
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
        logger.warning("Program terminated by user.")
    except Exception as e:
        console.print(f"[red]Fatal Error: {str(e)}[/red]")
        logger.critical(f"Fatal Error: {e}")
    finally:
        console.print(f"\n{APP_NAME} Session Terminated")
        logger.info("Application session terminated.")


if __name__ == "__main__":
    main()