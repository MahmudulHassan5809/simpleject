from collections.abc import Callable
from typing import Any, Optional

from .errors import ProviderNotFoundError
from .providers import FactoryProvider, SingletonProvider

_default_container: Optional["Container"] = None


def get_default_container() -> "Container":
    """Retrieve the global default container instance.

    Raises:
        RuntimeError: If no default container has been set yet.

    Returns:
        Container: The globally set default container instance.
    """
    if _default_container is None:
        raise RuntimeError("No default container set. Call container.set_default() first.")
    return _default_container


class Container:
    """Dependency Injection Container.

    Manages registration and resolution of providers for dependency injection,
    supporting singleton and factory providers, with both synchronous and asynchronous
    resolution by key or by type.

    Attributes:
        _providers (Dict[str, Any]): Maps keys to provider instances.
        _types (Dict[Type, str]): Maps types to their registered keys for type-based resolution.
    """

    def __init__(self) -> None:
        """Initialize an empty container."""
        self._providers: dict[str, Any] = {}
        self._types: dict[type, str] = {}

    def _infer_return_type(self, factory: Callable[[], Any]) -> type:
        """Infer the return type of a factory callable using type annotations.

        If annotation is missing, falls back to the type of the returned instance.

        Args:
            factory (Callable[[], Any]): The factory function to infer return type from.

        Returns:
            Type: The inferred return type of the factory.
        """
        # Use __annotations__['return'] if available, else call factory and get type
        return getattr(factory, "__annotations__", {}).get("return") or factory().__class__

    def register_singleton(self, key: str, factory: Callable[[], Any]) -> None:
        """Register a singleton provider with the given key and factory.

        The factory is called only once; subsequent resolutions return the cached instance.

        Args:
            key (str): The unique identifier for the provider.
            factory (Callable[[], Any]): A callable that returns an instance of the provided type.
        """
        self._providers[key] = SingletonProvider(factory)
        self._types[self._infer_return_type(factory)] = key

    def register_factory(self, key: str, factory: Callable[[], Any]) -> None:
        """Register a factory provider with the given key and factory.

        The factory is called every time the dependency is resolved.

        Args:
            key (str): The unique identifier for the provider.
            factory (Callable[[], Any]): A callable that returns a new instance on each call.
        """
        self._providers[key] = FactoryProvider(factory)
        self._types[self._infer_return_type(factory)] = key

    def resolve(self, key: str) -> Any:
        """Resolve a dependency synchronously by its registration key.

        Args:
            key (str): The unique provider key to resolve.

        Raises:
            ProviderNotFoundError: If no provider is registered under the given key.

        Returns:
            Any: The resolved instance.
        """
        provider = self._providers.get(key)
        if provider is None:
            raise ProviderNotFoundError(f"Provider '{key}' not found")
        return provider.get()

    async def aresolve(self, key: str) -> Any:
        """Resolve a dependency asynchronously by its registration key.

        This supports async singleton or factory providers.

        Args:
            key (str): The unique provider key to resolve.

        Raises:
            ProviderNotFoundError: If no provider is registered under the given key.

        Returns:
            Any: The resolved instance, awaited if async.
        """
        provider = self._providers.get(key)
        if provider is None:
            raise ProviderNotFoundError(f"Provider '{key}' not found")
        return await provider.aget()

    def resolve_by_type(self, cls: type) -> Any:
        """Resolve a dependency synchronously by its type.

        Args:
            cls (Type): The class/type to resolve.

        Raises:
            ProviderNotFoundError: If no provider is registered for the given type.

        Returns:
            Any: The resolved instance.
        """
        key = self._types.get(cls)
        if not key:
            raise ProviderNotFoundError(f"Provider for type '{cls.__name__}' not found")
        return self.resolve(key)

    async def aresolve_by_type(self, cls: type) -> Any:
        """Resolve a dependency asynchronously by its type.

        Args:
            cls (Type): The class/type to resolve.

        Raises:
            ProviderNotFoundError: If no provider is registered for the given type.

        Returns:
            Any: The resolved instance, awaited if async.
        """
        key = self._types.get(cls)
        if not key:
            raise ProviderNotFoundError(f"Provider for type '{cls.__name__}' not found")
        return await self.aresolve(key)

    def set_default(self) -> None:
        """Set this container instance as the global default container.

        This allows usage of the `@inject` decorator without manually passing container instance.
        """
        global _default_container
        _default_container = self
