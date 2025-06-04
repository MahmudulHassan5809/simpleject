import pytest

from simpleject.container import Container
from simpleject.decorators import inject


class Service:
    def __init__(self) -> None:
        self.called = True


@pytest.fixture(autouse=True)
def setup_container() -> None:
    container = Container()
    container.register_singleton("svc", lambda: Service())
    container.set_default()


def test_sync_injection() -> None:
    @inject
    def handler(svc: Service) -> Service:
        return svc

    instance = handler()  # pylint: disable=no-value-for-parameter
    assert isinstance(instance, Service)
    assert instance.called


@pytest.mark.asyncio
async def test_async_injection() -> None:
    @inject
    async def handler(svc: Service) -> Service:
        return svc

    instance = await handler()  # pylint: disable=no-value-for-parameter
    assert isinstance(instance, Service)
    assert instance.called
