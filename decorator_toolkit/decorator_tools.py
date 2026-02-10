"""Decorator tools."""

import functools
import logging
from datetime import datetime
from typing import TypeVar, ParamSpec, Callable


P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def log(msg: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log a function with the option for a custom message."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logging.debug(f"Called {func.__name__} with args={args} & kwargs={kwargs}")
            result = func(*args, **kwargs)
            logging.debug(f"{func.__name__} returned {result} ({type(result)})")
            if msg is not None:
                logging.info(msg)
            return result

        return wrapper

    return decorator


def timeit(func: Callable[P, R]) -> Callable[P, R]:
    """Print the time taken for a function to execute."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = datetime.now()
        result = func(*args, **kwargs)
        time_taken = datetime.now() - start
        milliseconds = time_taken.total_seconds() * 1000
        print(f"'{func.__name__}' took {round(milliseconds, 2)} milliseconds to run.")
        return result

    return wrapper

def memoize(func: Callable[P, R]) -> Callable[P, R]:
    """Cache."""
    cache: dict[tuple[tuple[object, ...], frozenset[tuple[str, object]]], R] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, frozenset(kwargs.items()))
        if key in cache:
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def validate(
    predicate: Callable[..., bool],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Validate a condition before calling function."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not predicate(*args, **kwargs):
                logging.error("Validation failed.")
                raise ValueError("Validation failed")
            return func(*args, **kwargs)

        return wrapper

    return decorator
