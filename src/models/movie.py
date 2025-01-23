class Movie:
    #constructor
    def __init__(self, movie_id, title, image, synopsis, duration, classification):
        self.movie_id = movie_id
        self.title = title
        self.image = image
        self.synopsis = synopsis
        self.duration = duration
        self.classification = classification

    #retornar un string con la informacion de la pelicula
    def __str__(self):
        return f"{self.title} ({self.duration} min) - {self.classification}\nSynopsis: {self.synopsis}"