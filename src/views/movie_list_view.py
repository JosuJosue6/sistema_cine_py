from tkinter import Frame, Label, Scrollbar, StringVar, Entry, Button, END, messagebox, Toplevel
from PIL import Image, ImageTk  # Necesitarás instalar Pillow para manejar imágenes
from models.movie import Movie
from controllers.movie_controller import MovieController
import os

class MovieListView(Frame):
    def __init__(self, master=None, db_connection=None):
        super().__init__(master)
        self.master = master
        self.movie_controller = MovieController(db_connection)
        self.selected_movie = StringVar()
        self.create_widgets()

    # Método para crear los widgets de la interfaz
    def create_widgets(self):
        self.title_label = Label(self, text="Cartelera de Películas", font=("Arial", 24))
        self.title_label.pack(pady=10)

        self.search_entry = Entry(self, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", self.filter_movies)

        self.movie_listbox = Frame(self)  # Cambiar Listbox a Frame para contener etiquetas
        self.movie_listbox.pack(pady=10)

        self.scrollbar = Scrollbar(self.movie_listbox)
        self.scrollbar.pack(side="right", fill="y")

        self.details_label = Label(self, text="", wraplength=600, justify="left")
        self.details_label.pack(pady=10)

        self.quit_button = Button(self, text="Salir", command=self.master.quit)
        self.quit_button.pack(pady=5)

        self.load_movies()

    # Método para cargar las películas en la lista
    def load_movies(self):
        movies = self.movie_controller.fetch_movies()
        print(f"Películas obtenidas: {movies}")  # Agregar esta línea para depuración
        for index, movie in enumerate(movies):
            print(f"Insertando película: {movie.title}")  # Agregar esta línea para depuración
            row = index // 4
            col = index % 4
            frame = Frame(self.movie_listbox, padx=25, pady=10)
            frame.pack(side="left", padx=25, pady=10)  # Usar pack en lugar de grid

            # Verificar si la imagen existe
            if os.path.exists(movie.image):
                # Cargar la imagen de la película
                image = Image.open(movie.image)
                image = image.resize((100, 150), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)

                image_label = Label(frame, image=photo)
                image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
                image_label.pack()

            title_label = Label(frame, text=movie.title, font=("Arial", 12), fg="black")
            title_label.pack()

            # Asociar el evento de clic para mostrar detalles
            frame.bind("<Button-1>", lambda e, m=movie: self.show_movie_details(m))

    # Método para filtrar las películas por título
    def filter_movies(self, event):
        query = self.search_entry.get().lower()
        for widget in self.movie_listbox.winfo_children():
            widget.destroy()
        movies = self.movie_controller.filter_movies(query)
        for index, movie in enumerate(movies):
            row = index // 4
            col = index % 4
            frame = Frame(self.movie_listbox, padx=25, pady=10)
            frame.pack(side="left", padx=25, pady=10)  # Usar pack en lugar de grid

            # Verificar si la imagen existe
            if os.path.exists(movie.image):
                # Cargar la imagen de la película
                image = Image.open(movie.image)
                image = image.resize((100, 150), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)

                image_label = Label(frame, image=photo)
                image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
                image_label.pack()

            title_label = Label(frame, text=movie.title, font=("Arial", 12), fg="black")
            title_label.pack()

            # Asociar el evento de clic para mostrar detalles
            frame.bind("<Button-1>", lambda e, m=movie: self.show_movie_details(m))

    # Método para mostrar los detalles de una película en una ventana emergente
    def show_movie_details(self, movie):
        popup = Toplevel(self)
        popup.title(movie.title)

        # Verificar si la imagen existe
        if os.path.exists(movie.image):
            # Cargar la imagen de la película
            image = Image.open(movie.image)
            image = image.resize((200, 300), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            image_label = Label(popup, image=photo)
            image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            image_label.pack(pady=10)

        details = f"Título: {movie.title}\nSinopsis: {movie.synopsis}\nGénero: {movie.genre}\nClasificación: {movie.classification}\nIdioma: {movie.language}\nDuración: {movie.duration} min"
        details_label = Label(popup, text=details, wraplength=400, justify="left")
        details_label.pack(pady=10)

        select_button = Button(popup, text="Seleccionar", command=lambda: self.select_movie(movie))
        select_button.pack(pady=5)

    # Método para seleccionar una película (puedes definir lo que hace)
    def select_movie(self, movie):
        messagebox.showinfo("Película seleccionada", f"Has seleccionado: {movie.title}")