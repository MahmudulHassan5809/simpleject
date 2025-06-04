from collections.abc import Awaitable, Callable
from typing import TypeVar

# Define a generic type variable to represent the return type of a provider
T = TypeVar('T')

# Synchronous provider function that returns a value of type T
ProviderFunc = Callable[[], T]

# Asynchronous provider function that returns an awaitable value of type T
AsyncProviderFunc = Callable[[], Awaitable[T]]
