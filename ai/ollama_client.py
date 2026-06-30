"""
LlamaPhone - Ollama AI Client
Wrapper for local Ollama LLM integration
"""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx


@dataclass
class ChatMessage:
    """Chat message structure."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass
class ToolDefinition:
    """Tool/function definition for the AI."""
    name: str
    description: str
    parameters: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }


class OllamaClient:
    """Client for Ollama local LLM API."""

    DEFAULT_BASE_URL = "http://localhost:11434"
    DEFAULT_MODEL = "qwen2.5-coder:7b"

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: float = 120.0
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)

        # Available tools
        self.tools: list[ToolDefinition] = []

        # Conversation history
        self.messages: list[ChatMessage] = []

    def is_available(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        """List available models in Ollama."""
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            pass
        return []

    def set_model(self, model: str):
        """Change the active model."""
        self.model = model

    def add_tool(self, tool: ToolDefinition):
        """Add a tool for the AI to use."""
        self.tools.append(tool)

    def add_tools(self, tools: list[ToolDefinition]):
        """Add multiple tools."""
        self.tools.extend(tools)

    def clear_history(self):
        """Clear conversation history."""
        self.messages = []

    def add_message(self, role: str, content: str):
        """Add a message to history."""
        self.messages.append(ChatMessage(role=role, content=content))

    def chat(
        self,
        message: str,
        system_prompt: str | None = None,
        stream: bool = False
    ) -> dict[str, Any]:
        """
        Send a chat message and get a response.

        Args:
            message: User message
            system_prompt: Optional system prompt override
            stream: Whether to stream the response

        Returns:
            Response dict with 'content', 'tool_calls', etc.
        """
        # Build messages list
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        elif self.messages:
            # Include history
            messages.extend([m.to_dict() for m in self.messages])

        messages.append({"role": "user", "content": message})

        # Prepare request
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": 0.7,
                "num_predict": 2048,
            }
        }

        # Add tools if available
        if self.tools:
            payload["tools"] = [t.to_dict() for t in self.tools]

        try:
            response = self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()

                # Add to history
                self.messages.append(ChatMessage(role="user", content=message))

                assistant_msg = result.get("message", {})
                self.messages.append(ChatMessage(
                    role="assistant",
                    content=assistant_msg.get("content", "")
                ))

                return {
                    "content": assistant_msg.get("content", ""),
                    "tool_calls": result.get("tool_calls", []),
                    "done": result.get("done", True),
                }
            else:
                return {
                    "content": f"Error: {response.status_code} - {response.text}",
                    "tool_calls": [],
                    "done": True
                }
        except Exception as e:
            return {
                "content": f"Connection error: {e!s}",
                "tool_calls": [],
                "done": True
            }

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        template: str | None = None
    ) -> str:
        """
        Generate text completion.

        Args:
            prompt: Input prompt
            system_prompt: Optional system prompt
            template: Optional custom template

        Returns:
            Generated text
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 2048,
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        if template:
            payload["template"] = template

        try:
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Connection error: {e!s}"

    def pull_model(self, model: str, progress_callback=None) -> bool:
        """
        Pull/download a model.

        Args:
            model: Model name to pull
            progress_callback: Optional callback(status, progress)

        Returns:
            True if successful
        """
        try:
            with self.client.stream(
                "POST",
                f"{self.base_url}/api/pull",
                json={"name": model},
                timeout=None
            ) as response:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        status = data.get("status", "")
                        progress = data.get("progress", 0)

                        if progress_callback:
                            progress_callback(status, progress)

                        if status == "success":
                            return True
            return False
        except Exception as e:
            print(f"Error pulling model: {e}")
            return False

    def create_model(
        self,
        name: str,
        modelfile_path: str
    ) -> bool:
        """
        Create a model from a Modelfile.

        Args:
            name: Name for the new model
            modelfile_path: Path to Modelfile

        Returns:
            True if successful
        """
        try:
            with open(modelfile_path) as f:
                modelfile_content = f.read()

            response = self.client.post(
                f"{self.base_url}/api/create",
                json={
                    "name": name,
                    "modelfile": modelfile_content
                }
            )

            return response.status_code == 200
        except Exception as e:
            print(f"Error creating model: {e}")
            return False

    def close(self):
        """Close the client connection."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LlamaPhoneAI:
    """
    LlamaPhone-specific AI wrapper with tools and prompts.
    """

    SYSTEM_PROMPT = """You are LlamaPhone, an expert AI assistant for mobile device repair.

You have access to tools for:
- ADB commands (connect, shell, install, push, pull, etc.)
- Fastboot commands (flash, unlock, reboot, etc.)
- Device diagnostics and information
- Script generation for automation

Guidelines:
1. Always prioritize device safety - warn before destructive operations
2. Explain what commands do before executing them
3. Provide step-by-step guidance when needed
4. Generate Python scripts when helpful for automation
5. Reference known exploits only for educational purposes on authorized devices

Commands you can help with:
- Device connection (USB/WiFi)
- FRP bypass procedures
- Bootloader unlock guides
- Root access setup (Magisk, Shizuku, etc.)
- Firmware flashing
- Debugging and diagnostics
- Custom script generation

Remember: Only assist with operations on devices you or your customer own!"""

    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client
        self.setup_tools()

    def setup_tools(self):
        """Setup available tools for the AI."""
        # ADB Tools
        from .tools.adb_tools import get_adb_tools
        self.client.add_tools(get_adb_tools())

        # Fastboot Tools
        from .tools.fastboot_tools import get_fastboot_tools
        self.client.add_tools(get_fastboot_tools())

        # Device Tools
        from .tools.device_tools import get_device_tools
        self.client.add_tools(get_device_tools())

    def chat(self, message: str) -> dict[str, Any]:
        """Send a chat message to the AI."""
        return self.client.chat(
            message=message,
            system_prompt=self.SYSTEM_PROMPT
        )

    def generate_script(self, task: str) -> str:
        """Generate a repair automation script."""
        prompt = f"""Generate a Python script for the following mobile repair task:

{task}

The script should:
1. Use subprocess to run ADB/fastboot commands
2. Include error handling
3. Have clear comments
4. Be production-ready

Only generate the Python code, no explanations.
"""
        return self.client.generate(prompt)
