import pytest

from simpleject.providers import FactoryProvider, SingletonProvider


class MyService:
    def __init__(self) -> None:
        self.count = 0


def factory() -> MyService:
    return MyService()


@pytest.mark.asyncio
async def test_singleton_provider() -> None:
    provider = SingletonProvider(factory)
    instance1 = provider.get()
    instance2 = provider.get()
    assert instance1 is instance2

    a_instance1 = await provider.aget()
    a_instance2 = await provider.aget()
    assert a_instance1 is a_instance2


@pytest.mark.asyncio
async def test_factory_provider() -> None:
    provider = FactoryProvider(factory)
    assert provider.get() is not provider.get()

    a1 = await provider.aget()
    a2 = await provider.aget()
    assert a1 is not a2
