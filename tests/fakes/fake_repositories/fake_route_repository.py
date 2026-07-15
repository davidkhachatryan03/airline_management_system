from src.entities import Route

class FakeRouteRepository:

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def insert_route(self, route: Route) -> None:
        self.routes.append(route)