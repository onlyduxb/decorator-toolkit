"""Decorator tools."""

import functools
import logging
from datetime import datetime
from typing import TypeVar, ParamSpec, Callable


P = ParamSpec("P")
R = TypeVar("R")


def log(msg: str | None = None, success_msg: str | None = None, failed_msg: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log the execution of a function.

    The decorator logs an optional base message when the function is called.
    If the wrapped function returns a truthy value, `success_msg` is logged.
    If it returns a falsy value, `failed_msg` is logged.

    Messages are only logged if provided. Exceptions raised by the wrapped
    function are not suppressed.

    Parameters
    ----------
    msg : str | None
        Message logged every time the function is called.
    success_msg : str | None
        Message logged when the wrapped function returns a truthy value.
    failed_msg : str | None
        Message logged when the wrapped function returns a falsy value.
    
    Example
    -------
    >>> import logging
    >>> logging.basicConfig(level=logging.INFO)
    >>>
    >>> @log(msg="Running check", success_msg="Passed", failed_msg="Failed")
    ... def is_even(x: int) -> bool:
    ...     return x % 2 == 0
    >>>
    >>> is_even(4)

    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logging.debug(f"Called {func.__name__} with args={args} & kwargs={kwargs}")
            result = func(*args, **kwargs)
            logging.debug(f"{func.__name__} returned {result} ({type(result)})")
            if msg is not None:
                logging.info(msg)
            if isinstance(result, bool):
                if result and success_msg:
                    logging.info(success_msg)
                elif not result and failed_msg:
                    logging.info(failed_msg)
            return result

        return wrapper

    return decorator


def timeit(func: Callable[P, R]) -> Callable[P, R]:
    """Measure execution time of a function.

    The decorator records how long the wrapped function takes to execute
    and reports the duration. The original return value of the function
    is preserved.

    The timing mechanism measures total runtime from function entry to exit.
    Exceptions raised by the wrapped function are not suppressed.

    Parameters
    ----------
    func : Callable[P, R]
        The function whose execution time will be measured.

    Returns
    -------
    Callable[P, R]
        A wrapped function with identical signature and return value.

    Example
    -------
    >>> @timeit
    ... def slow_operation() -> None:
    ...     import time
    ...     time.sleep(1)
    ...
    >>> slow_operation()

    """

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
    """Cache function results based on input arguments.

    The decorator stores results from previous calls and returns the cached
    value when the function is called again with the same arguments.
    This avoids repeated computation for identical inputs.

    Cached values persist for the lifetime of the program unless explicitly
    cleared by the implementation.

    Parameters
    ----------
    func : Callable[P, R]
        The function whose results will be cached.

    Returns
    -------
    Callable[P, R]
        A wrapped function with identical signature and return value.

    Example
    -------
    >>> @memoize
    ... def fibonacci(n: int) -> int:
    ...     if n < 2:
    ...         return n
    ...     return fibonacci(n - 1) + fibonacci(n - 2)
    ...
    >>> fibonacci(30)

    """
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
    condition: Callable[..., bool],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Enforce a validation condition before function execution.

    The decorator factory accepts a condition function that is evaluated
    using the same arguments passed to the wrapped function. If the condition
    evaluates to True, the function executes normally. If it evaluates to
    False, execution is prevented and an exception is raised.

    The wrapped function’s signature and return value are preserved.

    Parameters
    ----------
    condition : Callable[..., bool]
        A callable that receives the same arguments as the wrapped function
        and returns True if execution is allowed, or False otherwise.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        A decorator that applies the validation check.

    Example
    -------
    >>> def not_negative(x: float) -> bool:
    ...     if x >= 0:
    ...         return True
    ...     else:
    ...         return False
    ...
    >>> @validate(not_negative)
    ... def sqrt(x: float) -> float:
    ...     return x ** 0.5
    ...
    >>> sqrt(9)
    >>> sqrt(-1)  # validation fails

    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not condition(*args, **kwargs):
                logging.error("Validation failed.")
                raise ValueError("Validation failed")
            return func(*args, **kwargs)

        return wrapper

    return decorator