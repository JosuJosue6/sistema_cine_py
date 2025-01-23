from tkinter import Frame, Label, Listbox, Scrollbar, StringVar, Entry, Button, END
from tkinter import messagebox
from models.movie import Movie
from controllers.movie_controller import MovieController

class MovieListView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.movie_controller = MovieController()
        self.selected_movie = StringVar()
        self.create_widgets()

    #metodo para crear los widgets de la interfaz
    def create_widgets(self):
        self.title_label = Label(self, text="Cartelera de Películas", font=("Arial", 24))
        self.title_label.pack(pady=10)

        self.search_entry = Entry(self, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", self.filter_movies)

        self.movie_listbox = Listbox(self, width=80, height=20)
        self.movie_listbox.pack(pady=10)

        self.scrollbar = Scrollbar(self.movie_listbox)
        self.scrollbar.pack(side="right", fill="y")
        self.movie_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.movie_listbox.yview)

        self.movie_listbox.bind('<<ListboxSelect>>', self.display_movie_details)

        self.details_label = Label(self, text="", wraplength=600, justify="left")
        self.details_label.pack(pady=10)

        self.quit_button = Button(self, text="Salir", command=self.master.quit)
        self.quit_button.pack(pady=5)

        self.load_movies()

    #metodo para cargar las peliculas en la lista
    def load_movies(self):
        movies = self.movie_controller.get_all_movies()
        for movie in movies:
            self.movie_listbox.insert(END, movie.title)

    #metodo para filtrar las peliculas por titulo
    def filter_movies(self, event):
        query = self.search_entry.get().lower()
        self.movie_listbox.delete(0, END)
        movies = self.movie_controller.get_filtered_movies(query)
        for movie in movies:
            self.movie_listbox.insert(END, movie.title)

    #metodo para mostrar los detalles de una pelicula
    def display_movie_details(self, event):
        selected_index = self.movie_listbox.curselection()
        if selected_index:
            movie_title = self.movie_listbox.get(selected_index)
            movie = self.movie_controller.get_movie_by_title(movie_title)
            details = f"Título: {movie.title}\nSinopsis: {movie.synopsis}\nDuración: {movie.duration} min"
            self.details_label.config(text=details)
        else:
            self.details_label.config(text="")