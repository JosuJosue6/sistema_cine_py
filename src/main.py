from tkinter import Tk
from database.db_connection import DatabaseConnection
from views.login_view import LoginView

def main():
    root = Tk()
    root.title("Test")
    root.geometry("1800x1080")

    # Conexión a la DB
    server = r'JOSUJOSUELAPTOP\SQLEXPRESS'
    database = 'CINE'
    username = 'sa'
    password = 'josueNSD6'

    db_connection = DatabaseConnection(server, database, username, password)
    db_connection.connect()
    
    # Crear la vista de la lista de películas y pasar la conexión de la base de datos
    login_view = LoginView(root, db_connection)
    # Empaquetar la vista
    login_view.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()