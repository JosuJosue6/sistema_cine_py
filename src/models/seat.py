class Seat:
    # Constructor
    def __init__(self, room, row, number, availability=True):
        self.room = room
        self.row = row
        self.number = number
        self.availability = availability

     #retornar un string con la informacion del asiento
    def is_available(self):
        return self.availability

     #reservar el asiento
    def reserve(self):
        if self.availability:
            self.availability = False
            return True
        return False

    #liberar el asiento
    def release(self):
        self.availability = True

    #retornar un string con la informacion del asiento
    def __str__(self):
        return f"Room: {self.room}, Row: {self.row}, Number: {self.number}, Availability: {self.availability}"