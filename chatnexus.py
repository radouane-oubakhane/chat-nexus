import sys
import re
from difflib import get_close_matches
from typing import List, Dict, Optional

import ollama
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress
from rich.prompt import Prompt, Confirm

console = Console()
APP_NAME = "[bold cyan]ChatNexus[/bold cyan]"
COMMAND_LIST = ['/models', '/download', '/switch', '/settings', '/history', '/exit', '/help']


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
            console.print(f"[bold]{APP_NAME} Session Ended[/bold]")
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


def validate_model_name(model_name: str) -> Optional[str]:
    """Sanitize and validate the model name."""
    model_name = model_name.strip().lower()
    if not model_name:
        console.print("[red]Error: Model name cannot be empty[/red]")
        return None
    if '/' not in model_name:
        console.print("[yellow]⚠ Hint: Use format 'author/modelname' for better results[/yellow]")
    return model_name


def download_model(model_name: str) -> Optional[str]:
    """Download a model from Ollama with validation and progress display."""
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


class ThinkingProcessor:
    """Processes and displays <think>...</think> blocks."""

    def __init__(self, console: Console):
        self.console = console
        self.buffer = []
        self.thinking = False

    def process_chunk(self, content: str) -> str:
        """Extract and display thinking blocks, returning the remaining text."""
        if '<think>' in content and '</think>' in content:
            # Single chunk containing both tags
            thinking_text = re.search(r'<\s*think\s*>(.*?)<\s*/\s*think\s*>', content, re.IGNORECASE | re.DOTALL)
            if thinking_text:
                clean_text = thinking_text.group(1).strip()
                self.display_thinking(clean_text)
                content = re.sub(r'<\s*think\s*>.*?<\s*/\s*think\s*>', '', content, flags=re.IGNORECASE | re.DOTALL)
        elif '<think>' in content:
            # Start of thinking block
            self.thinking = True
            thinking_part = content.split('<think>')[1]
            self.buffer.append(thinking_part.strip())
            content = content.split('<think>')[0]
        elif '</think>' in content and self.thinking:
            # End of thinking block
            thinking_part = content.split('</think>')[0]
            self.buffer.append(thinking_part.strip())
            thinking_text = ' '.join(self.buffer).strip()
            self.display_thinking(thinking_text)
            self.buffer.clear()
            self.thinking = False
            content = content.split('</think>')[1]
        elif self.thinking:
            # Continuation of thinking block
            self.buffer.append(content.strip())
            content = ''
        return content

    def display_thinking(self, text: str) -> None:
        """Display the thinking text in a styled panel if not empty."""
        if text:
            self.console.print(
                Panel(
                    f"[italic]{text}[/italic]",
                    title="[yellow]💭 Thinking Process[/yellow]",
                    border_style="yellow",
                    padding=(1, 2)
                )
            )


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
            if Confirm.ask("Restart chat session?"):
                self.history.clear()
                return None
            return None


def main():
    """Main entry point of the application."""
    history: List[Dict[str, str]] = []
    current_model: Dict[str, str] = {'name': None}

    try:
        display_welcome()
        model_name = model_selection()
        if not model_name:
            console.print("[red]No model selected. Exiting...[/red]")
            return

        current_model['name'] = model_name
        console.print(f"\n[green]Active Model: {model_name}[/green]")
        chat = ChatInterface(current_model, history)
        chat.chat_loop()

    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Fatal Error: {str(e)}[/red]")
    finally:
        console.print(f"\n{APP_NAME} Session Terminated")


if __name__ == "__main__":
    main()