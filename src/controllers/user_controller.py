class UserController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # CRUD básico de usuarios
    # Crear un nuevo usuario
    def create_user(self, user_data):
        query = "INSERT INTO Users (name, email, password) VALUES (?, ?, ?)"
        self.db_connection.execute_query(query, (user_data['name'], user_data['email'],  user_data['password']))
        self.db_connection.commit()

    # Buscar usuario por su ID
    def get_user(self, user_id):
        query = "SELECT * FROM Users WHERE ID = ?"
        return self.db_connection.execute_query(query, (user_id,)).fetchone()

    # Obtener correo de usuario por ID
    def get_user_email(self, user_id):
        query = "SELECT email FROM Users WHERE ID = ?"
        return self.db_connection.execute_query(query, (user_id,)).fetchone()

    # Actualizar los datos de un usuario
    def update_user(self, user_id, user_data):
        query = "UPDATE Users SET name = ?, email = ?, phone = ?, password = ? WHERE ID = ?"
        self.db_connection.execute_query(query, (user_data['name'], user_data['email'], user_data['phone'], user_data['password'], user_id))
        self.db_connection.commit()

    # Eliminar un usuario
    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE ID = ?"
        self.db_connection.execute_query(query, (user_id,))
        self.db_connection.commit()

    # Obtener el historial de compras de un usuario
    def get_purchase_history(self, user_id):
        query = "SELECT * FROM Purchases WHERE user_id = ?"
        return self.db_connection.execute_query(query, (user_id,)).fetchall()

    # Obtener usuario por correo electrónico
    def get_user_by_email(self, email):
        query = "SELECT * FROM Users WHERE email = ?"
        return self.db_connection.execute_query(query, (email,)).fetchone()

    # Autenticar usuario
    def authenticate_user(self, email, password):
        query = "SELECT * FROM Users WHERE email = ? AND password = ?"
        user = self.db_connection.execute_query(query, (email, password))
        if user:
            print(f"Bienvenido, {user}!")
            return True
        else:
            print("Correo electrónico o contraseña incorrectos.")
            return False
        #return 

    # Obtener todos los usuarios
    def get_all_users(self):
        query = "SELECT * FROM Users"
        return self.db_connection.execute_query(query).fetchall()