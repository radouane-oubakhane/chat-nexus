import re

from rich.console import Console
from rich.panel import Panel

console = Console()


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