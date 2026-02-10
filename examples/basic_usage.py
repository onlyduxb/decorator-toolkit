"""Basic examples for decorator toolkit."""

from decorator_toolkit import log, timeit, memoize, validate
import logging

logging.basicConfig(
    filename="debugger.log",
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

@log('Said hello to a person.')
def say_hello(name: str) -> None:
    """Log example."""
    print(f'Hello, {name}!')

@memoize
@timeit
def fibonacci(n: int) -> int:
    """Memory and timeit example."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def not_zero(a: float) -> bool:
    """Dependency for validate example."""
    return a >= 0

@validate(not_zero)
def sqrt(a: float) -> float:
    """Validate example."""
    return a**0.5