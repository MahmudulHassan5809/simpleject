import asyncio
from collections.abc import Callable
from threading import Lock
from typing import Any


class SingletonProvider:
    """A provider that ensures a singleton instance of a given dependency.

    It supports both synchronous and asynchronous initialization. If the factory
    function returns a coroutine, it will be awaited during async resolution.

    Attributes:
        _factory (Callable[[], Any]): A function that returns the dependency instance.
        _instance (Any): Cached singleton instance.
        _lock (Lock): Thread-safe lock for sync instantiation.
        _async_lock (asyncio.Lock): Async lock to prevent concurrent creation in async context.
    """

    def __init__(self, factory: Callable[[], Any]):
        self._factory = factory
        self._instance = None
        self._lock = Lock()
        self._async_lock = asyncio.Lock()

    def get(self) -> Any:
        """Returns the singleton instance (sync context).
        If the instance does not exist, it will be created using the factory.
        """
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._factory()
        return self._instance

    async def aget(self) -> Any:
        """Returns the singleton instance (async context).
        If the instance does not exist, it will be created using the factory.
        Handles coroutine factories as well.
        """
        if self._instance is None:
            async with self._async_lock:
                if self._instance is None:
                    result = self._factory()
                    # Await if factory returns a coroutine
                    self._instance = await result if asyncio.iscoroutine(result) else result
        return self._instance


class FactoryProvider:
    """A provider that returns a new instance of a dependency on each request.

    It supports both synchronous and asynchronous creation.

    Attributes:
        _factory (Callable[[], Any]): A function that returns a new instance each time.
    """

    def __init__(self, factory: Callable[[], Any]):
        self._factory = factory

    def get(self) -> Any:
        """Returns a new instance (sync context) by calling the factory."""
        return self._factory()

    async def aget(self) -> Any:
        """Returns new instance(async context) by calling  factory.Handles coroutine factories."""
        result = self._factory()
        return await result if asyncio.iscoroutine(result) else result
