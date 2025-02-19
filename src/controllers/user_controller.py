from models.user import User

class UserController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # CRUD básico de usuarios
    # Crear un nuevo usuario
    def create_user(self, user_data):
        query = "INSERT INTO Users (name, lastname, CI, email, password) VALUES (?, ?, ?, ?, ?)"
        self.db_connection.execute_query(query, (user_data['name'], user_data['lastname'], user_data['CI'], user_data['email'], user_data['password']))
        self.db_connection.commit()

    # Buscar usuario por su ID
    def get_user(self, user_id):
        query = "SELECT * FROM Users WHERE ID = ?"
        cursor = self.db_connection.execute_query(query, (user_id,))
        result = cursor.fetchone()
        if result:
            user_data = [field if field is not None else "" for field in result]
            return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5])
        return None

    # Actualizar los datos de un usuario
    def update_user(self, user_id, user_data):
        query = "UPDATE Users SET name = ?, lastname = ?, CI = ?, email = ?, password = ? WHERE ID = ?"
        self.db_connection.execute_query(query, (user_data['name'], user_data['lastname'], user_data['CI'], user_data['email'], user_data['password'], user_id))
        self.db_connection.commit()

    # Eliminar un usuario
    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE ID = ?"
        self.db_connection.execute_query(query, (user_id,))
        self.db_connection.commit()


    # Autenticar usuario
    def authenticate_user(self, email, password):
        query = "SELECT * FROM Users WHERE email = ? AND password = ?"
        cursor = self.db_connection.execute_query(query, (email, password))
        result = cursor.fetchone()
        if result:
           # print(result)
            #print("******",User(result[0], result[1], result[5], result[6], result[2], result[4]))
            return User(result[0], result[1], result[2], result[3], result[4], result[5])
        return None

    # Obtener el ID de un usuario por su correo electrónico
    def get_id_by_email(self, email):
        query = "SELECT ID FROM Users WHERE email = ?"
        cursor = self.db_connection.execute_query(query, (email,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None