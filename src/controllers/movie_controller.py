from models.movie import Movie


class MovieController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # CRUD básico de películas
    # buscar todas las películas
    def fetch_movies(self):
        query = "SELECT * FROM Movies"
        #print(self.db_connection.server)
        result = self.db_connection.execute_query(query)
       # print(result)
        if result:
            return [Movie(*row) for row in result]
        return []

    # buscar películas por género, clasificación o idioma
    def filter_movies(self, genre=None, classification=None, language=None, title=None):
        query = "SELECT * FROM Movies WHERE 1=1"
        if genre:
            query += f" AND genre='{genre}'"
        if classification:
            query += f" AND classification='{classification}'"
        if language:
            query += f" AND Languaje='{language}'"
        if title:
            query += f" AND title LIKE '%{title}%'"
        result = self.db_connection.execute_query(query)
        if result:
            return [Movie(*row) for row in result]
        return []

    # buscar los detalles de una película por su id
    def get_movie_details(self, movie_id):
        query = f"SELECT * FROM Movies WHERE ID={movie_id}"
        result = self.db_connection.execute_query(query)
        if result:
            return Movie(*result[0])
        return None

    # agregar una nueva película
    def add_movie(self, title, image, synopsis, duration, genre, classification, language):
        query = f"INSERT INTO Movies (title, image, synopsis, duration, genre, classification, language) VALUES ('{title}', '{image}', '{synopsis}', {duration}, '{genre}', '{classification}', '{language}')"
        self.db_connection.execute_query(query)

    # actualizar los datos de una película
    def update_movie(self, movie_id, title, image, synopsis, duration, genre, classification, language):
        query = f"UPDATE Movies SET title='{title}', image='{image}', synopsis='{synopsis}', duration={duration}, genre='{genre}', classification='{classification}', language='{language}' WHERE ID={movie_id}"
        self.db_connection.execute_query(query)

    # eliminar una película
    def delete_movie(self, movie_id):
        query = f"DELETE FROM Movies WHERE ID={movie_id}"
        self.db_connection.execute_query(query)