class AbstractSites:
    def get(self, username: str):
        raise NotImplemented()

    def get_planet(self, username: str, planet: str):
        raise NotImplemented()

    def planets(self, username: str):
        raise NotImplemented()
