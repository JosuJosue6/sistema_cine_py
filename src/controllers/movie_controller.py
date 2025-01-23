class MovieController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    #CRUD basico de peliculas
    #buscar todas las peliculas
    def fetch_movies(self):
        query = "SELECT * FROM Movies"
        return self.db_connection.execute_query(query)

    #buscar peliculas por genero, clasificacion o idioma
    def filter_movies(self, genre=None, classification=None, language=None):
        query = "SELECT * FROM Movies WHERE 1=1"
        if genre:
            query += f" AND genre='{genre}'"
        if classification:
            query += f" AND classification='{classification}'"
        if language:
            query += f" AND language='{language}'"
        return self.db_connection.execute_query(query)

    #buscar los detalles de una pelicula por su id
    def get_movie_details(self, movie_id):
        query = f"SELECT * FROM Movies WHERE ID={movie_id}"
        return self.db_connection.execute_query(query)

    #agregar una nueva pelicula
    def add_movie(self, title, image, synopsis, duration, classification):
        query = f"INSERT INTO Movies (title, image, synopsis, duration, classification) VALUES ('{title}', '{image}', '{synopsis}', {duration}, '{classification}')"
        self.db_connection.execute_query(query)

    #actualizar los datos de una pelicula
    def update_movie(self, movie_id, title, image, synopsis, duration, classification):
        query = f"UPDATE Movies SET title='{title}', image='{image}', synopsis='{synopsis}', duration={duration}, classification='{classification}' WHERE ID={movie_id}"
        self.db_connection.execute_query(query)

    #eliminar una pelicula
    def delete_movie(self, movie_id):
        query = f"DELETE FROM Movies WHERE ID={movie_id}"
        self.db_connection.execute_query(query)