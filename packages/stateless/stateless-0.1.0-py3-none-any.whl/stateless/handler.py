from typing import (
    Generic,
    TypeVar,
    Any,
    Dict,
    Type,
    get_type_hints,
    get_args,
    get_origin,
)
from types import UnionType
from abc import ABC, abstractmethod

from stateless.action import Action
from stateless.effect import Effect


A = TypeVar("A", bound=Action)
A2 = TypeVar("A2", bound=Action)
R = TypeVar("R")


class Handler(Generic[A], ABC):
    @abstractmethod
    def handle(self, action: A) -> Any:
        pass

    def __and__(self, other: "Handler[A2]") -> "Handler[A | A2]":
        return CompositeHandler(self, other)

    def run(self, es: Effect[A, Exception, R]) -> R:
        next(es)
        while True:
            try:
                es.send(self.handle)
            except StopIteration as e:
                return e.value


A3 = TypeVar("A3", bound=Action)


class CompositeHandler(Handler[A3]):
    handlers: Dict[Type[Action], Handler]

    def __init__(self, first: Handler[A], second: Handler[A2]) -> None:
        handlers: Dict[Type[Action], Handler] = {}
        if isinstance(first, CompositeHandler):
            handlers.update(first.handlers)
        elif isinstance(first, Handler):
            e_type = list(get_type_hints(first.handle).values())[0]
            if isinstance(e_type, UnionType):
                for t in get_args(e_type):
                    t = get_origin(t) or t
                    handlers[t] = first
            else:
                e_type = get_origin(e_type) or e_type
                handlers[e_type] = first

        if isinstance(second, CompositeHandler):
            handlers.update(second.handlers)
        elif isinstance(second, Handler):
            e_type = get_type_hints(second.handle)["action"]
            if isinstance(e_type, UnionType):
                for t in get_args(e_type):
                    t = get_origin(t) or t
                    handlers[t] = second
            else:
                e_type = get_origin(e_type) or e_type
                handlers[e_type] = second

        self.handlers = handlers

    def handle(self, effect: A3) -> Any:
        handler = self.handlers[type(effect)]
        return handler.handle(effect)

    def run(self, es: Effect[A, Exception, R]) -> R:
        effect = next(es)
        while True:
            try:
                if isinstance(effect, Exception):
                    effect = es.send(lambda _: effect)
                else:
                    effect = es.send(self.handlers[type(effect)].handle)
            except StopIteration as e:
                return e.value
