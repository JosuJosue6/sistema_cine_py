from tkinter import Tk
from database.db_connection import DatabaseConnection
from views.movie_list_view import MovieListView

def main():
    root = Tk()
    root.title("Test")
    root.geometry("800x600")

    # Conexión a la DB
    server = r'JOSUJOSUELAPTOP\SQLEXPRESS'
    database = 'CINE'
    username = 'sa'
    password = 'josueNSD6'

    db_connection = DatabaseConnection(server, database, username, password)
    db_connection.connect()
    
    # Crear la vista de la lista de películas y pasar la conexión de la base de datos
    movie_list_view = MovieListView(root, db_connection)
    # Empaquetar la vista
    movie_list_view.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()