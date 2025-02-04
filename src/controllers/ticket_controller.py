class TicketController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    #CRUD basico de tickets
    #buscar todos los tipos de tickets
    def get_ticket_types(self):
        # Fetch ticket types and prices from the database
        query = "SELECT type, price FROM tickets"
        result = self.db_connection.execute_query(query)
        # Convertir el resultado a una lista de diccionarios
        ticket_types = [{'type': row[0], 'price': row[1]} for row in result]
        return ticket_types

    #calcular el precio total de un ticket
    def calculate_price(self, ticket_type, quantity, promotions):
        ticket_info = self.get_ticket_types()
        price = next((item['price'] for item in ticket_info if item['type'] == ticket_type), 0)
        total_price = price * quantity

        #aplicar promociones al precio total si hubiese
        if promotions:
            total_price = self.apply_promotions(total_price, promotions)

        return total_price

    #aplicar promociones al precio total
    def apply_promotions(self, total_price, promotions):
        #aplicar promociones
        for promo in promotions:
            if promo['type'] == 'percentage':
                total_price -= total_price * (promo['value'] / 100)
            elif promo['type'] == 'fixed':
                total_price -= promo['value']
        return total_price

    #crear un nuevo ticket
    def create_ticket(self, user_id, movie_id, ticket_type, quantity, total_price):
        #query para insertar un nuevo ticket en la base de datos
        query = "INSERT INTO tickets (user_id, movie_id, type, quantity, total_price) VALUES (?, ?, ?, ?, ?)"
        params = (user_id, movie_id, ticket_type, quantity, total_price)
        self.db_connection.execute_query(query, params)

    #buscar los tickets de un usuario
    def get_user_tickets(self, user_id):
        #query para buscar los tickets de un usuario
        query = "SELECT * FROM tickets WHERE user_id = ?"
        return self.db_connection.execute_query(query, (user_id,))