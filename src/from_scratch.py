class Bike:
    """Already written for you. Do not change it."""

    def __init__(self, serial, station, needs_repair):
        self.serial = serial
        self.station = station
        self.needs_repair = needs_repair

    def is_rentable(self):
        return not self.needs_repair

    def __repr__(self):
        return f"Bike({self.serial!r})"


class Member:
    """Already written for you. Do not change it."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Member({self.name!r})"


class Rental:
    pass


class BikeShare:
    pass


class Repair:
    pass


class Station:
    pass
