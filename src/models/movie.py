class Movie:
    #constructor
    def __init__(self, movie_id, title, image, synopsis, duration, classification, genre, language):
        self.movie_id = movie_id
        self.title = title
        self.image = image
        self.synopsis = synopsis
        self.duration = duration
        self.classification = classification
        self.genre = genre
        self.language = language


    #retornar un string con la informacion de la pelicula
    def __str__(self):
        return f"{self.title} ({self.duration} min) - {self.classification}\nSynopsis: {self.synopsis} - Genre: {self.genre} - Language: {self.language}"