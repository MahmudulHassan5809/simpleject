import pytest

from simpleject.container import Container, get_default_container
from simpleject.errors import ProviderNotFoundError


class MyService:
    pass


def service_factory() -> MyService:
    return MyService()


def test_register_and_resolve_singleton() -> None:
    container = Container()
    container.register_singleton("svc", service_factory)
    resolved = container.resolve("svc")
    assert isinstance(resolved, MyService)
    assert resolved is container.resolve("svc")


def test_register_and_resolve_factory() -> None:
    container = Container()
    container.register_factory("svc", service_factory)
    assert isinstance(container.resolve("svc"), MyService)
    assert container.resolve("svc") is not container.resolve("svc")


def test_resolve_by_type() -> None:
    container = Container()
    container.register_singleton("svc", service_factory)
    instance = container.resolve_by_type(MyService)
    assert isinstance(instance, MyService)


def test_set_default_container() -> None:
    container = Container()
    container.set_default()
    assert get_default_container() is container


def test_provider_not_found() -> None:
    container = Container()
    with pytest.raises(ProviderNotFoundError):
        container.resolve("missing")

    with pytest.raises(ProviderNotFoundError):
        container.resolve_by_type(str)
