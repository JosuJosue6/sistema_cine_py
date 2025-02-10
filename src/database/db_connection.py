import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    # Conexión a la base de datos
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            )
            print("Conección exitosa ****************************************")
        except Exception as e:
            print(f"Error: {e}")

    # Ejecutar una query
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    # Cerrar la conexión
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")