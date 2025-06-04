from simpleject import Container, inject


class MyService:
    def greet(self) -> str:
        return "Hello from MyService"


container = Container()
container.register_singleton("my_service", lambda: MyService())
container.set_default()


@inject
def handler(my_service: MyService) -> None:
    print(my_service.greet())


handler()  # pylint: disable=no-value-for-parameter
