

```shell
pip install cosmoai
```

```shell
cosmo
```

<br>

**CosmoAI** lets LLMs run code (Python, Javascript, Shell, and more) locally. You can chat with CosmoAI through a ChatGPT-like interface in your terminal by running `$ cosmo` after installing.

This provides a natural-language interface to your computer's general-purpose capabilities:

- Create and edit photos, videos, PDFs, etc.
- Control a Chrome browser to perform research
- Plot, clean, and analyze large datasets
- ...etc.

**⚠️ Note: You'll be asked to approve code before it's run.**

<br>

## Demo

https://github.com/SerHermes

#### An interactive demo is also available on Google Colab:

[![Open In Colab]()

#### Along with an example implementation of a voice interface (inspired by _Her_):

[![Open In Colab]()

## Quick Start

```shell
pip install cosmoai
```

### Terminal

After installation, simply run `cosmo`:

```shell
cosmo
```

### Python

```python
import cosmo

cosmo.chat("Plot AAPL and META's normalized stock prices") # Executes a single command
cosmo.chat() # Starts an interactive chat
```

## Comparison to ChatGPT's Code Interpreter

OpenAI's release of [Code Interpreter](https://openai.com/blog/chatgpt-plugins#code-Interpreter) with GPT-4 presents a fantastic opportunity to accomplish real-world tasks with ChatGPT.

However, OpenAI's service is hosted, closed-source, and heavily restricted:

- No internet access.
- [Limited set of pre-installed packages](https://wfhbrian.com/mastering-chatgpts-code-cosmo-list-of-python-packages/).
- 100 MB maximum upload, 120.0 second runtime limit.
- State is cleared (along with any generated files or links) when the environment dies.

---

CosmoAI overcomes these limitations by running in your local environment. It has full access to the internet, isn't restricted by time or file size, and can utilize any package or library.

This combines the power of GPT-4's Code Cosmo with the flexibility of your local development environment.

## Commands

**Update:** The Generator Update (0.1.5) introduced streaming:

```python
message = "What operating system are we on?"

for chunk in cosmo.chat(message, display=False, stream=True):
  print(chunk)
```

### Interactive Chat

To start an interactive chat in your terminal, either run `cosmo` from the command line:

```shell
cosmo
```

Or `cosmo.chat()` from a .py file:

```python
cosmo.chat()
```

**You can also stream each chunk:**

```python
message = "What operating system are we on?"

for chunk in cosmo.chat(message, display=False, stream=True):
  print(chunk)
```

### Programmatic Chat

For more precise control, you can pass messages directly to `.chat(message)`:

```python
cosmo.chat("Add subtitles to all videos in /videos.")

# ... Streams output to your terminal, completes task ...

cosmo.chat("These look great but can you make the subtitles bigger?")

# ...
```

### Start a New Chat

In Python, CosmoAI remembers conversation history. If you want to start fresh, you can reset it:

```python
cosmo.reset()
```

### Save and Restore Chats

`cosmo.chat()` returns a List of messages, which can be used to resume a conversation with `cosmo.messages = messages`:

```python
messages = cosmo.chat("My name is Henry.") # Save messages to 'messages'
cosmo.reset() # Reset cosmo ("Henry" will be forgotten)

cosmo.messages = messages # Resume chat from 'messages' ("Henry" will be remembered)
```

### Customize System Message

You can inspect and configure CosmoAI's system message to extend its functionality, modify permissions, or give it more context.

```python
cosmo.system_message += """
Run shell commands with -y so the user doesn't have to confirm them.
"""
print(cosmo.system_message)
```

### Change your Language Model

CosmoAI uses [LiteLLM](https://docs.litellm.ai/docs/providers/) to connect to hosted language models.

You can change the model by setting the model parameter:

```shell
cosmo --model gpt-3.5-turbo
cosmo --model claude-2
cosmo --model command-nightly
```

In Python, set the model on the object:

```python
cosmo.model = "gpt-3.5-turbo"
```

[Find the appropriate "model" string for your language model here.](https://docs.litellm.ai/docs/providers/)

### Running CosmoAI locally

CosmoAI uses [LM Studio](https://lmstudio.ai/) to connect to local language models (experimental).

Simply run `cosmo` in local mode from the command line:

```shell
cosmo --local
```

**You will need to run LM Studio in the background.**

1. Download [https://lmstudio.ai/](https://lmstudio.ai/) then start it.
2. Select a model then click **↓ Download**.
3. Click the **↔️** button on the left (below 💬).
4. Select your model at the top, then click **Start Server**.

Once the server is running, you can begin your conversation with CosmoAI.

(When you run the command `cosmo --local`, the steps above will be displayed.)

> **Note:** Local mode sets your `context_window` to 3000, and your `max_tokens` to 600. If your model has different requirements, set these parameters manually (see below).

#### Context Window, Max Tokens

You can modify the `max_tokens` and `context_window` (in tokens) of locally running models.

For local mode, smaller context windows will use less RAM, so we recommend trying a much shorter window (~1000) if it's is failing / if it's slow. Make sure `max_tokens` is less than `context_window`.

```shell
cosmo --local --max_tokens 1000 --context_window 3000
```

### Debug mode

To help contributors inspect CosmoAI, `--debug` mode is highly verbose.

You can activate debug mode by using it's flag (`cosmo --debug`), or mid-chat:

```shell
$ cosmo
...
> %debug true <- Turns on debug mode

> %debug false <- Turns off debug mode
```

### Interactive Mode Commands

In the interactive mode, you can use the below commands to enhance your experience. Here's a list of available commands:

**Available Commands:**

- `%debug [true/false]`: Toggle debug mode. Without arguments or with `true` it
  enters debug mode. With `false` it exits debug mode.
- `%reset`: Resets the current session's conversation.
- `%undo`: Removes the previous user message and the AI's response from the message history.
- `%save_message [path]`: Saves messages to a specified JSON path. If no path is provided, it defaults to `messages.json`.
- `%load_message [path]`: Loads messages from a specified JSON path. If no path is provided, it defaults to `messages.json`.
- `%tokens [prompt]`: (_Experimental_) Calculate the tokens that will be sent with the next prompt as context and estimate their cost. Optionally calculate the tokens and estimated cost of a `prompt` if one is provided. Relies on [LiteLLM's `cost_per_token()` method](https://docs.litellm.ai/docs/completion/token_usage#2-cost_per_token) for estimated costs.
- `%help`: Show the help message.

### Configuration

CosmoAI allows you to set default behaviors using a `config.yaml` file.

This provides a flexible way to configure the cosmo without changing command-line arguments every time.

Run the following command to open the configuration file:

```
cosmo --config
```

#### Multiple Configuration Files

CosmoAI supports multiple `config.yaml` files, allowing you to easily switch between configurations via the `--config_file` argument.

**Note**: `--config_file` accepts either a file name or a file path. File names will use the default configuration directory, while file paths will use the specified path.

To create or edit a new configuration, run:

```
cosmo --config --config_file $config_path
```

To have CosmoAI load a specific configuration file run:

```
cosmo --config_file $config_path
```

**Note**: Replace `$config_path` with the name of or path to your configuration file.

##### CLI Example

1. Create a new `config.turbo.yaml` file
   ```
   cosmo --config --config_file config.turbo.yaml
   ```
2. Edit the `config.turbo.yaml` file to set `model` to `gpt-3.5-turbo`
3. Run CosmoAI with the `config.turbo.yaml` configuration
   ```
   cosmo --config_file config.turbo.yaml
   ```

##### Python Example

You can also load configuration files when calling CosmoAI from Python scripts:

```python
import os
import cosmo

currentPath = os.path.dirname(os.path.abspath(__file__))
config_path=os.path.join(currentPath, './config.test.yaml')

cosmo.extend_config(config_path=config_path)

message = "What operating system are we on?"

for chunk in cosmo.chat(message, display=False, stream=True):
  print(chunk)
```

## Sample FastAPI Server

The generator update enables CosmoAI to be controlled via HTTP REST endpoints:

```python
# server.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cosmo

app = FastAPI()

@app.get("/chat")
def chat_endpoint(message: str):
    def event_stream():
        for result in cosmo.chat(message, stream=True):
            yield f"data: {result}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/history")
def history_endpoint():
    return cosmo.messages
```

```shell
pip install fastapi uvicorn
uvicorn server:app --reload
```

## Safety Notice

Since generated code is executed in your local environment, it can interact with your files and system settings, potentially leading to unexpected outcomes like data loss or security risks.

**⚠️ CosmoAI will ask for user confirmation before executing code.**

You can run `cosmo -y` or set `cosmo.auto_run = True` to bypass this confirmation, in which case:

- Be cautious when requesting commands that modify files or system settings.
- Watch CosmoAI like a self-driving car, and be prepared to end the process by closing your terminal.
- Consider running CosmoAI in a restricted environment like Google Colab or Replit. These environments are more isolated, reducing the risks of executing arbitrary code.

There is **experimental** support for a [safe mode](docs/SAFE_MODE.md) to help mitigate some risks.

## How Does it Work?

CosmoAI equips a [function-calling language model](https://platform.openai.com/docs/guides/gpt/function-calling) with an `exec()` function, which accepts a `language` (like "Python" or "JavaScript") and `code` to run.

We then stream the model's messages, code, and your system's outputs to the terminal as Markdown.

# Contributing

Thank you for your interest in contributing! We welcome involvement from the community.

Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to get involved.

## License

CosmoAI is licensed under the MIT License. You are permitted to use, copy, modify, distribute, sublicense, and sell copies of the software.

**Note**: This software is not affiliated with OpenAI.

> Having access to a junior programmer working at the speed of your fingertips ... can make new workflows effortless and efficient, as well as open the benefits of programming to new audiences.
>
> — _OpenAI's Code Cosmo Release_

<br>
