import datetime
import os
import time
from typing import override

from askui.agent_base import AgentBase
from askui.models.shared.tools import Tool
from askui.tools.agent_os import AgentOs
from askui.tools.toolbox import AgentToolbox


class SaveScreenshotTool(Tool):
    """
    Save a screenshot of the current screen to disk.
    """

    def __init__(self, agent_os: AgentOs, base_dir: str):
        super().__init__(
            name="save_screenshot_tool",
            description="Save a screenshot of the current screen to disk.",
            input_schema={
                "type": "object",
                "properties": {
                    "directory_name": {
                        "type": "string",
                        "description": "The name of the directory to save the screenshot to.",
                    },
                    "image_name": {
                        "type": "string",
                        "description": "The name of the image to save without the png extension.",
                    },
                },
                "required": ["directory_name", "image_name"],
            },
        )
        self._agent_os = agent_os
        self._base_dir = base_dir

    @override
    def __call__(self, directory_name: str, image_name: str) -> str:
        relative_image_path = os.path.join(f"{directory_name}", f"{image_name}.png")
        absolute_image_path = os.path.join(self._base_dir, relative_image_path)
        os.makedirs(os.path.dirname(absolute_image_path), exist_ok=True)
        image = self._agent_os.screenshot()
        image.save(absolute_image_path)
        return f"screenshot of the current screen saved to {relative_image_path}. it must be added to the markdown file as evidence with the following format: ![ScreenshotName](./{relative_image_path})"


class WaitTool(Tool):
    """
    Waits for a specified amount of time in seconds.
    """

    def __init__(self):
        super().__init__(
            name="wait_tool",
            description="Waits for a specified amount of time in seconds.",
            input_schema={
                "type": "object",
                "properties": {
                    "milliseconds": {
                        "type": "integer",
                        "description": "The number of milliseconds to wait. It can be a decimal number. For example, 500 is half a second. max is 60000 milliseconds.",
                    },
                },
                "required": ["milliseconds"],
            },
        )

    @override
    def __call__(self, milliseconds: int) -> str:
        if not isinstance(milliseconds, int):
            raise ValueError("Milliseconds must be an integer.")
        if milliseconds < 0:
            raise ValueError("Milliseconds cannot be negative.")
        if milliseconds > 60000:
            raise ValueError("Milliseconds cannot be greater than 60000.")
        time.sleep(milliseconds / 1000)
        return f"Waited for {milliseconds} milliseconds."


class GetCurrentTimeTool(Tool):
    """
    Get the current time in UTC.
    """

    def __init__(self):
        super().__init__(
            name="get_current_time_tool",
            description="This tool can be used to retrieve the current time. No input is required.",
            input_schema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )

    @override
    def __call__(self) -> str:
        return f"Current UTC time: {datetime.datetime.now(datetime.UTC).strftime('%A, %B %d, %Y at %H:%M:%S UTC')}"


class FileReadTool(Tool):
    """
    Reads content from a file in the base directory.
    """

    def __init__(self, absolute_file_path: str):
        if not os.path.isfile(absolute_file_path):
            raise RuntimeError(f"File not found: {absolute_file_path}")
        file_name = (
            os.path.basename(absolute_file_path)
            .strip()
            .replace(" ", "_")
            .replace(".", "_")
            .lower()
        )
        super().__init__(
            name=f"file_read_tool_{file_name}",
            description="Reads content from a file.",
        )
        self._absolute_file_path = absolute_file_path

    @override
    def __call__(self) -> str:
        if not os.path.isfile(self._absolute_file_path):
            raise FileNotFoundError(f"File not found: {self._absolute_file_path}")
        with open(self._absolute_file_path, "r", encoding="utf-8") as f:
            return f.read()


class FileWriteTool(Tool):
    """
    Writes content to a file in the base directory. Overwrites if the file already exists.
    """

    def __init__(self, base_dir: str):
        super().__init__(
            name="file_write_tool",
            description="Writes content to a file in the base directory. It works with append mode. If the file does not exist, it will be created.",
            input_schema={
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "Relative path to the file to write to.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to append to the file.",
                    },
                },
                "required": ["file_name", "content"],
            },
        )
        self._base_dir = base_dir
        os.makedirs(self._base_dir, exist_ok=True)

    @override
    def __call__(self, file_name: str, content: str) -> str:
        file_path = os.path.join(self._base_dir, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")
        return f"Content was written successfully to {file_name}"


class FileListTool(Tool):
    """
    Lists all files in the base directory.
    """

    def __init__(self, base_dir: str):
        super().__init__(
            name="list_files_tool",
            description="Lists all files in the base directory.",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the directory to list files from.",
                    },
                },
                "required": ["path"],
            },
        )
        self._base_dir = base_dir

    @override
    def __call__(self, path: str) -> str:
        directory_path = os.path.join(self._base_dir, path)
        if not os.path.exists(directory_path):
            raise RuntimeError(f"Directory '{path}' does not exist.")
        files = os.listdir(directory_path)
        return f"Files in '{path}' directory: {files}"


class PrintTool(Tool):
    """
    A tool that can be used to print the content to the console.
    """

    def __init__(self, source_name: str):
        super().__init__(
            name="print_tool",
            description="A tool that can be used to print the content to the console. To update the user about the current state of the execution.",
            input_schema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to print to the console.",
                    },
                },
                "required": ["content"],
            },
        )
        self._source_name = source_name

    @override
    def __call__(self, content: str) -> str:
        print(f"[{self._source_name}]: {content}")
        return "Content was printed to the console."


class OpenBrowserTool(Tool):
    """
    Opens a browser.
    """

    def __init__(self, agent_toolbox: AgentToolbox):
        super().__init__(
            name="open_browser_tool",
            description="Opens a browser.",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Relative path to the file to write to.",
                    },
                },
                "required": ["url"],
            },
        )
        self._agent_toolbox = agent_toolbox

    @override
    def __call__(self, url: str) -> str:
        self._agent_toolbox.webbrowser.open(url)
        return f"Browser opened successfully to {url}"

class AskUIGetMethodTool(Tool):
    """
    A tool that can be used to get information from an image based on the provided query.
    """

    def __init__(self, askui_agent: AgentBase):
        super().__init__(
            name="askui_get_method_tool",
            description="It retrieves information from an image based on the provided query",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query describing what information to retrieve.",
                    },
                },
                "required": ["query"],
            },
        )
        self._askui_agent = askui_agent

    @override
    def __call__(self, query: str) -> str:
        return self._askui_agent.get(query, response_schema=str)
