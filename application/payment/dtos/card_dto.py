from domain.card import Card


class CardDTO:
    def __init__(self, card: Card):
        self.id = card.id
        self.titular = card.titular
        self.brand = card.brand.value
        self.final = card.final()
        self.method = card.method.value
        self.due_date = card.due_date.strftime("%Y-%m-%d")
        self.cvv = card.cvv
