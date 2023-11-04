from typing import Any, TypeVar
from collections.abc import Generator

from stateless.action import Action

A = TypeVar("A", bound=Action)
E = TypeVar("E", bound=Exception)
R = TypeVar("R")

# TODO: how to avoid accumulating very long union types?
Effect = Generator[A | E, Any, R]
Depend = Generator[A, Any, R]
Try = Generator[E, Any, R]
