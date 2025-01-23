class Ticket:
    #constructor
    def __init__(self, ticket_type, price, promotions=None):
        self.ticket_type = ticket_type
        self.price = price
        self.promotions = promotions if promotions is not None else []

    #aplicar promociones al precio del ticket
    def apply_promotions(self):
        #sumar el descuento de todas las promociones
        total_discount = sum(p.discount for p in self.promotions)
        self.price -= total_discount

    #retornar un string con la informacion del ticket
    def __str__(self):
        return f"Ticket(type={self.ticket_type}, price={self.price}, promotions={self.promotions})"