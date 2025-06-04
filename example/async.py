import asyncio

from simpleject import Container, inject


class MyService:
    async def greet(self) -> str:
        await asyncio.sleep(0.1)  # Simulate async work
        return "Hello from async MyService"


# Set up the container
container = Container()
container.register_singleton("my_service", lambda: MyService())
container.set_default()


@inject
async def handler(my_service: MyService) -> None:
    msg = await my_service.greet()
    print(msg)


# Run the async handler
asyncio.run(handler())  # pylint: disable=no-value-for-parameter
