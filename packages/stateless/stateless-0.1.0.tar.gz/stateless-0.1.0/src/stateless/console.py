from typing_extensions import Never
from dataclasses import dataclass

from stateless.action import Action
from stateless.handler import Handler


@dataclass(frozen=True)
class Print(Action[Never, None]):
    content: str


@dataclass(frozen=True)
class Input(Action[Never, str]):
    prompt: str = ""


Console = Print | Input


class LiveConsole(Handler[Console]):
    def handle(self, action: Console) -> str | None:
        match action:
            case Print(content):
                print(content)
                return None
            case Input(prompt):
                return input(prompt)
