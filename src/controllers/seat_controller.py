from models.seat import Seat

class SeatController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # Obtener todos los asientos disponibles
    def get_seats(self):
        query = "SELECT * FROM seats"
        result = self.db_connection.execute_query(query)
        if result is None:
            print("No se obtuvieron resultados de la consulta.")
            return []
        print(f"Resultados de la consulta: {result}")
        seats = [Seat(row[1], row[2], row[3]) for row in result]
        return seats

    # Obtener todos los asientos disponibles
    def get_available_seats(self):
        query = "SELECT * FROM seats WHERE available = 1"
        result = self.db_connection.execute_query(query)
        if result is None:
            print("No se obtuvieron resultados de la consulta.")
            return []
        print(f"Resultados de la consulta: {result}")
        seats = [Seat(row[0], row[1], row[2], row[3]) for row in result]
        return seats

    # Reservar un asiento
    def reserve_seat(self, room, row, number):
        query = "UPDATE seats SET available = 0 WHERE room = ? AND row = ? AND number = ? AND available = 1"
        params = (room, row, number)
        result = self.db_connection.execute_query(query, params)
        return result.rowcount > 0

    # Liberar un asiento
    def release_seat(self, room, row, number):
        query = "UPDATE seats SET available = 1 WHERE room = ? AND row = ? AND number = ?"
        params = (room, row, number)
        self.db_connection.execute_query(query, params)

    # Validar la selección de asientos
    def validate_seat_selection(self, room, selected_seats):
        available_seats = self.get_available_seats(room)
        return all(seat in available_seats for seat in selected_seats)