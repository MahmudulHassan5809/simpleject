# Python Dependency Injection Container

A lightweight, production-ready Dependency Injection (DI) framework for Python with support for singleton and factory providers, sync/async resolution, and function injection.

## 🚀 Features

- Singleton and factory providers for flexible dependency management
- Automatic injection via type annotations
- Support for synchronous and asynchronous functions
- Zero dependencies (pure Python standard library)
- `@inject` decorator with or without parentheses
- Manual support for nested dependencies
- Built using [`uv`](https://docs.astral.sh/uv/) for modern Python packaging

## 📋 Requirements

- Python 3.8 or higher
- Optional: `uv` for package management
- Optional: `pytest` for running tests

## 📦 Installation

Install the package using `uv` or `pip`:

```bash
uv add simpleject  # Replace with actual package name
# OR
pip install simpleject
```

## 🧱 Project Structure

```
your_di_package/
├── pyproject.toml       # Project metadata and dependencies
├── uv.toml             # UV configuration for package management
├── src/                # Source code directory
│   ├── __init__.py     # Package initialization
│   ├── container.py    # Core DI container logic
│   ├── providers.py    # Singleton and factory provider implementations
│   ├── errors.py       # Custom error definitions
│   └── inject.py       # Injection decorator and utilities
├── tests/              # Test suite
│   └── test_di.py      # Unit tests for DI functionality
└── README.md           # Project documentation
```

## ✨ Usage

### 1. Define a Service

Create a service class to be injected:

```python
# my_service.py
class MyService:
    def greet(self) -> str:
        return "Hello from MyService!"
```

### 2. Register in the Container

Register the service in the DI container:

```python
from src.container import Container
from my_service import MyService

container = Container()
container.register_singleton("my_service", lambda: MyService())
container.set_default()
```

### 3. Inject Dependencies

Use the `@inject` decorator to inject dependencies:

```python
from src.inject import inject
from my_service import MyService

@inject
def handler(my_service: MyService):
    print(my_service.greet())

handler()  # Output: Hello from MyService!
```

### 4. Async Support

Handle asynchronous services and functions:

```python
import asyncio
from src.inject import inject

class AsyncService:
    async def greet(self) -> str:
        return "Hello async world!"

container.register_singleton("async_service", lambda: AsyncService())

@inject
async def async_handler(async_service: AsyncService):
    print(await async_service.greet())

asyncio.run(async_handler())  # Output: Hello async world!
```

### 5. Nested Dependencies

Manually resolve nested dependencies in factories:

```python
class Repo:
    pass

class Service:
    def __init__(self, repo: Repo):
        self.repo = repo

container.register_singleton("repo", lambda: Repo())
container.register_singleton("service", lambda: Service(container.resolve("repo")))
```

## 🧪 Testing

Install testing dependencies:

```bash
uv add --dev pytest
uv lock
```

Run tests:

```bash
uv run pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/your-username/your-di-package). Ensure tests pass and follow the coding style.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
