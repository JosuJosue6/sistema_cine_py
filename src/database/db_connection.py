import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    #coneccion a la base de datos
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            )
            print("Connection successful")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    #ejecutar una query
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    #cerrar la conexion
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")