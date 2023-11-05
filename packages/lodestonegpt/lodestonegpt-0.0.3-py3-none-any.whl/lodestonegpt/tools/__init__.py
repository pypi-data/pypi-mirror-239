from lodestonegpt.tools.agent_manager import (
    CreateAgent,
    MessageAgent,
    DeleteAgent,
    ListAgents,
)
from lodestonegpt.tools.user_manager import AskUser
from lodestonegpt.tools.base_tool import BaseTool
from lodestonegpt.tools.browser import Browser
from lodestonegpt.tools.code import ExecutePythonFile, ReviewCode, ImproveCode, WriteTests
from lodestonegpt.tools.math import EvaluateMath
from lodestonegpt.tools.google_search import GoogleSearch
from lodestonegpt.tools.filesystem import (
    ReadFromFile,
    WriteToFile,
    AppendToFile,
    DeleteFile,
    CheckIfFileExists,
    ListFiles,
    GetCWD,
    MakeDirectory,
    FileSystemTools,
)
from lodestonegpt.tools.shell import Shell
from lodestonegpt.tools.memory_manager import AddToMemory


user_tools = {}


def register_tool_type(tool):
    if isinstance(tool, BaseTool):
        tool = tool.__class__
    if not isinstance(tool, type):
        raise TypeError(f"{tool} is not a class")
    if not issubclass(tool, BaseTool):
        raise TypeError(f"{tool} does not inherit from BaseTool")
    user_tools[tool.__name__] = tool


def from_config(config) -> BaseTool:
    class_name = config["class"]
    clss = user_tools.get(class_name) or globals()[class_name]
    return clss.from_config(config)


def builtin_tools():
    return [
        GoogleSearch,
        Browser,
        CreateAgent,
        MessageAgent,
        ListAgents,
        DeleteAgent,
        *FileSystemTools,
        ReviewCode,
        ImproveCode,
        WriteTests,
        ExecutePythonFile,
        EvaluateMath,
        AskUser,
        Shell,
    ]
