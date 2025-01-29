import re
from typing import List, Dict, Optional

from rich.console import Console
from rich.panel import Panel

import ollama
from rich.progress import Progress
from rich.prompt import Prompt

from processor import ThinkingProcessor  # New module
from utils import validate_model_name

console = Console()
APP_NAME = "[bold cyan]ChatNexus[/bold cyan]"


class ChatInterface:
    """Handles the main chat interactions."""

    def __init__(self, current_model: Dict[str, str], history: List[Dict[str, str]]):
        self.console = Console()
        self.processor = ThinkingProcessor(self.console)
        self.current_model = current_model
        self.history = history

    def chat_loop(self) -> None:
        """Main loop for handling user input and AI responses."""
        while True:
            try:
                user_input = Prompt.ask(f"\n{APP_NAME} :: {self.current_model['name']}")
                if user_input.startswith('/'):
                    from commands import handle_command  # Avoid circular imports
                    if not handle_command(user_input, self.history, self.current_model):
                        break
                    continue

                response = self.get_ai_response(user_input)
                if response:
                    self.history.extend([
                        {'role': 'user', 'content': user_input},
                        {'role': 'assistant', 'content': response}
                    ])

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Chat session ended[/yellow]")
                break

    def get_ai_response(self, user_input: str) -> Optional[str]:
        """Fetch and display the AI response."""
        from processor import ThinkingProcessor  # Avoid circular imports

        try:
            with Progress(transient=True) as progress:
                progress.add_task("[cyan]🤔 Processing...", total=None)
                response = ollama.chat(
                    model=self.current_model['name'],
                    messages=[{'role': 'user', 'content': user_input}],
                    stream=True
                )

            self.console.print("\n[bold cyan]AI:[/bold cyan]")
            full_response = ""

            for chunk in response:
                content = chunk['message']['content']
                returned_text = self.processor.process_chunk(content)
                if returned_text:
                    print(returned_text, end='', flush=True)
                    full_response += returned_text

            print('\n')
            return full_response

        except Exception as e:
            self.console.print(f"\n[red]Error: {str(e)}[/red]")
            from rich.prompt import Confirm
            if Confirm.ask("Restart chat session?"):
                self.history.clear()
                return None
            return None