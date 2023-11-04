from typing_extensions import Never
from dataclasses import dataclass

from stateless.action import Action
from stateless.handler import Handler


@dataclass(frozen=True)
class ReadFile(Action[FileNotFoundError | PermissionError, str]):
    path: str


@dataclass(frozen=True)
class WriteFile(Action[Never, None]):
    path: str
    content: str


Files = ReadFile | WriteFile


class LiveFiles(Handler[Files]):
    def handle(self, action: Files) -> FileNotFoundError | None | str:
        match action:
            case ReadFile(path):
                try:
                    with open(path, "r") as f:
                        return f.read()
                except FileNotFoundError as e:
                    return e
            case WriteFile(path, content):
                with open(path, "w") as f:
                    f.write(content)
                return None
