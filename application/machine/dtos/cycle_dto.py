from application.util.currency import br
from domain.cycle import Cycle


class CycleDTO:
    def __init__(self, cycle: Cycle):
        self.id = cycle.id
        self.time = cycle.time
        self.price = cycle.price

    def get_formatted_price(self):
        return br(self.price)