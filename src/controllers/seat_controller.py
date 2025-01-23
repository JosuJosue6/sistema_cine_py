class SeatController:
    def __init__(self, seat_model):
        self.seat_model = seat_model

    #obtener todos los asientos disponibles
    def get_available_seats(self, room):
        return self.seat_model.get_available_seats(room)

    #reservar un asiento
    def reserve_seat(self, room, row, number):
        if self.seat_model.is_seat_available(room, row, number):
            self.seat_model.reserve_seat(room, row, number)
            return True
        return False

    #liberar un asiento
    def release_seat(self, room, row, number):
        self.seat_model.release_seat(room, row, number)

    #validar la seleccion de asientos
    def validate_seat_selection(self, room, selected_seats):
        available_seats = self.get_available_seats(room)
        return all(seat in available_seats for seat in selected_seats)