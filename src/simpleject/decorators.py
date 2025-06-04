import asyncio
import inspect
from collections.abc import Callable
from functools import wraps

from .container import Container, get_default_container


def inject(func_or_container: Callable | Container | None = None) -> Callable:
    """Decorator to automatically inject dependencies into a function
    based on its type annotations using a DI container.

    Usage:
        @inject
        def handler(service: MyService): ...

        @inject(container)
        def handler(service: MyService): ...

        @inject()
        def handler(service: MyService): ...
    """
    # Case: @inject(container)
    if isinstance(func_or_container, Container):

        def wrapper(func: Callable) -> Callable:
            return _wrap_function(func, func_or_container)

        return wrapper

    # Case: @inject
    if callable(func_or_container):
        return _wrap_function(func_or_container, get_default_container())

    # Case: @inject()
    def default_wrapper(func: Callable) -> Callable:
        return _wrap_function(func, get_default_container())

    return default_wrapper


def _wrap_function(func: Callable, container: Container) -> Callable:
    """Internal utility to wrap a function with injected dependencies.

    Args:
        func: The target function to wrap.
        container: The DI container to resolve dependencies from.

    Returns:
        A wrapped version of the function with dependencies injected
        based on type annotations.
    """
    sig = inspect.signature(func)
    is_async = asyncio.iscoroutinefunction(func)

    @wraps(func)
    def sync_wrapper(*args: list, **kwargs: dict) -> Callable:
        """Wrapper for sync functions that resolves and injects missing dependencies."""
        # Bind partial args to identify which params are already provided
        bound = sig.bind_partial(*args, **kwargs)
        for name, param in sig.parameters.items():
            # Inject only if argument is missing and has a type annotation
            if name not in bound.arguments and param.annotation != inspect.Parameter.empty:
                kwargs[name] = container.resolve_by_type(param.annotation)
        return func(*args, **kwargs)

    @wraps(func)
    async def async_wrapper(*args: list, **kwargs: dict) -> Callable:
        """Wrapper for async functions that resolves and injects missing dependencies asynchronously."""
        bound = sig.bind_partial(*args, **kwargs)
        for name, param in sig.parameters.items():
            if name not in bound.arguments and param.annotation != inspect.Parameter.empty:
                kwargs[name] = await container.aresolve_by_type(param.annotation)
        return await func(*args, **kwargs)

    return async_wrapper if is_async else sync_wrapper
