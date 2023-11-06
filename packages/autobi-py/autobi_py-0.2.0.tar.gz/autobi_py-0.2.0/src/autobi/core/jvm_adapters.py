import functools
from typing import Any, Type, TypeVar, Callable

from pathlib import Path

T = TypeVar("T")
F = TypeVar("F")
SelfType = TypeVar("SelfType")


def to_java_float(f: float) -> str:
    """Takes a float, returns a string of that float with 6 digits of presision"""
    return f"{f:.6f}"


def to_java_bool(b: bool) -> str:
    """returns 'true' or 'false' instead of 'True' and 'False'"""
    return str(b).lower()


def to_resolved_path_str(path: Path) -> str:
    "Takes a path, resolves the path, then returns the string representation of the path"
    return str(path.resolve())


def base_str(a: Any) -> str:
    "A seperate `str` method made into a seperate object such that `takes` can test for it"
    return str(a)


def takes(
    t: Type[T], *, converter: Callable[[T], str] = base_str
) -> Callable[[Callable[[SelfType, str], F]], Callable[[SelfType, T], F]]:
    """Wraps a method inside a JVM-interfacing class
    Allows the exposed method to take in the specified type that has a __str__,
    then converts any passed argument into a string before passing it to the main func
    """
    if converter is base_str and not "__str__" in dir(t):
        raise ValueError(f"Cannot parse arguments of type {t} to str")

    def wrap(f: Callable[[SelfType, str], F]) -> Callable[[SelfType, T], F]:
        @functools.wraps(f)
        def inner(self: SelfType, arg: T) -> F:
            return f(self, converter(arg))

        return inner

    return wrap
