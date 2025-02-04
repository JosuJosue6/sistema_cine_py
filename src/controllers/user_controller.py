class UserController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

#CRUD basico de usuarios
    #crear un nuevo usuario
    def create_user(self, user_data):
        query = "INSERT INTO Users (name, email, phone) VALUES (?, ?, ?)"
        self.db_connection.execute_query(query, (user_data['name'], user_data['email'], user_data['phone']))
        self.db_connection.commit()

    #buscar usuario por su id
    def get_user(self, user_id):
        query = "SELECT * FROM Users WHERE ID = ?"
        return self.db_connection.execute_query(query, (user_id,))

    #obtener correo usuario por id

    def get_user_email(self, user_id):
        query = "SELECT email FROM Users WHERE ID = ?"
        return self.db_connection.execute_query(query, (user_id,))

    #actualizar los datos de un usuario
    def update_user(self, user_id, user_data):
        query = "UPDATE Users SET name = ?, email = ?, phone = ? WHERE ID = ?"
        self.db_connection.execute_query(query, (user_data['name'], user_data['email'], user_data['phone'], user_id))
        self.db_connection.commit()

    #eliminar un usuario
    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE ID = ?"
        self.db_connection.execute_query(query, (user_id,))
        self.db_connection.commit()

    #obtener el historial de compras de un usuario
    def get_purchase_history(self, user_id):
        query = "SELECT * FROM Purchases WHERE user_id = ?"
        return self.db_connection.execute_query(query, (user_id,))