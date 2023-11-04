from typing import Generic, TypeVar, Callable
from collections.abc import Generator

from typing_extensions import Self


E = TypeVar("E", bound=Exception, covariant=True)
R = TypeVar("R", covariant=True)

A = TypeVar("A", bound="Action")

Handler = Callable[[A], E | R]


class Action(Generic[E, R]):
    def __iter__(
        self: Self,
    ) -> Generator[Self | E, Handler[Self, E, R], R]:
        handler = yield self
        result = handler(self)
        if isinstance(result, Exception):
            # TODO: how to avoid missing return statement?
            yield result  # type: ignore
        else:
            return result

    def catch(self) -> Generator[Self, Handler[Self, E, R], E | R]:
        handler = yield self
        return handler(self)

    def or_die(self) -> Generator[Self, Handler[Self, E, R], R]:
        handler = yield self
        result = handler(self)
        if isinstance(result, Exception):
            raise result
        else:
            return result
