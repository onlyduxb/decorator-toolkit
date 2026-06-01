# decorator-toolkit

Type-safe Python decorators for logging, timing, memoization, and input validation.

## Installation
pip install decorator-toolkit
(Available at: https://pypi.org/project/decorator-toolkit/#description)

## Quick example
```py
from decorator_toolkit import log, timeit

@log("Multiplied a number by two.")
@timeit
def times_two(x: int) -> int:
    return x * 2
```
