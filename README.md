# Chat Nexus

Chat Nexus is an AI-powered terminal application that offers an interactive chat experience. Manage your AI models, engage in conversations, and keep track of your chat history—all from your command line.

## Features

- **Model Management**: List, download, and switch between different AI models.
- **Interactive Chat**: Engage in intelligent conversations with the AI.
- **Conversation History**: View your past interactions.
- **User-Friendly Interface**: Enhanced terminal UI with rich formatting.

## Installation

### Prerequisites

- **Python 3.8+**
- **Git**

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/radouane-oubakhane/chat-nexus.git
   cd chat-nexus
   ```

2. **Set Up a Virtual Environment**

    ```bash
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment**

    - **Windows**

      ```bash
      venv\Scripts\activate
      ```

    - **macOS/Linux**

      ```bash
      source venv/bin/activate
      ```

4. **Install the Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the following command to start the application:

```bash
python main.py
```

Follow the on-screen prompts to select a model, start a chat, view history, or exit the application.

Available commands:

- `/models`: List all installed AI models
- `/download`: Download a new AI model
- `/switch`: Change the active AI model
- `/history`: View conversation history
- `/help`: Show help information
- `/exit`: Quit the application
