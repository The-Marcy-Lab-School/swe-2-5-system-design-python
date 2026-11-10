class Depot:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self._items = []

    def store(self, serial):
        if len(self._items) >= self.capacity:
            raise ValueError(f"{self.name} is full.")
        self._items.append(serial)

    def count(self):
        return len(self._items)

    def contents(self):
        return self._items


class Checkout:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.total = 0
        self.status = "open"

    def add(self, serial, price):
        if self.status != "open":
            raise ValueError(f"add needs an open checkout, not {self.status}.")
        self.items.append((serial, price))

    def complete(self):
        self.status = "complete"
        self.total = sum(price for _, price in self.items)
        if not self.items:
            raise ValueError("A checkout needs at least one item.")
        return self.total
