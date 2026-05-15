from abc import ABC, abstractmethod

class Seat(ABC):
    def __init__(self, viewer: str):
        self.viewer = viewer

    @abstractmethod
    def ticket_price(self) -> int:
        pass

class Standard(Seat):
    def ticket_price(self) -> int:
        return 35_000

class Premium(Seat):
    def ticket_price(self) -> int:
        return 70_000

class Vip(Seat):
    def ticket_price(self) -> int:
        return 120_000


class Ticket(ABC):
    @abstractmethod
    def print_ticket(self, bookings: list):
        pass
class PaperTicket(Ticket):
    def print_ticket(self, bookings: list):
        for seat in bookings:
            print(f"TICKET <{seat.viewer}> price={seat.ticket_price()}")

class QrSender(ABC):
    @abstractmethod
    def send(self, bookings: list):
        pass

class TelegramQrSender(QrSender):
    def send(self, bookings: list):
        for seat in bookings:
            print(f"[QR → {seat.viewer}] Show this at entrance. Paid {seat.ticket_price()} so'm")


class TicketSystem:
    def __init__(self):
        self.bookings = []

    def add(self, seat: Seat):
        self.bookings.append(seat)

    def run(self, ticket_printer: Ticket, qr_sender: QrSender):
        ticket_printer.print_ticket(self.bookings)
        qr_sender.send(self.bookings)


cinema = TicketSystem()
cinema.add(Standard("Anakin"))
cinema.add(Premium("Obi-Wan"))
cinema.add(Vip("Yoda"))

cinema.run(PaperTicket(), TelegramQrSender())