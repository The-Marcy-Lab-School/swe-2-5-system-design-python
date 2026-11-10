class BoroBikes:
    def __init__(self):
        self.bikes = []

    def add_bike(self, serial):
        self.bikes.append(serial)

    def fleet_size(self):
        return len(self.bikes)

    def invoice_total(self, minutes):
        return round(minutes * 0.25, 2)

    def invoice_text(self, minutes, name):
        return f"{name} owes {self.invoice_total(minutes)}"

    def repair_priority(self, serial):
        return "urgent" if serial.startswith("BROKEN") else "normal"

    def rota_for(self, name, days):
        return f"{name} works {days} days"


class Invoice:
    """Give this the two invoice jobs."""
    pass


class Mechanic:
    """Give this the two mechanic jobs."""
    pass


class Book:
    def __init__(self, title):
        self.title = title
        self.on_loan = False

    def lend_to(self, reader):
        if self.on_loan:
            raise ValueError(f"{self.title} is already out.")
        self.on_loan = True
        reader.loans.append(self)
        return f"{reader.name} borrowed {self.title}"


class Reader:
    def __init__(self, name):
        self.name = name
        self.loans = []

    def loan_count(self):
        return len(self.loans)

    def borrow(self, book):
        if len(self.loans) >= 3:
            raise ValueError(f"{self.name} already has three books.")
        book.on_loan = True
        self.loans.append(book)
        return f"{self.name} borrowed {book.title}"


class Library:
    """Give this the one rule both classes were enforcing halves of."""

    def lend(self, reader, book):
        pass


class Delivery:
    def __init__(self, serial):
        self.serial = serial
        self.status = "packed"

    def pack(self):
        if self.status != "new":
            raise ValueError(f"pack needs a new delivery, not {self.status}.")
        self.status = "packed"

    def collect(self):
        if self.status != "packed":
            raise ValueError(f"collect needs a packed delivery, not {self.status}.")
        self.status = "collected"

    def deliver(self):
        self.status = "delivered"
