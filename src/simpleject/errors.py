class DIError(Exception):
    """Base exception class for all Dependency Injection related errors.
    """
    pass


class ProviderNotFoundError(DIError):
    """Exception raised when a provider for a given key is not found in the container.

    Attributes:
        key (str): The key for which the provider was not found.
    """

    def __init__(self, key: str):
        """Initialize the ProviderNotFoundError with the missing provider key.

        Args:
            key (str): The key for the provider that was not found.
        """
        super().__init__(f"Provider not found for key: {key}")
        self.key = key


class CircularDependencyError(DIError):
    """Exception raised when a circular dependency is detected during dependency resolution.

    Circular dependencies occur when two or more providers depend on each other directly
    or indirectly, causing an infinite loop.
    """
    pass
