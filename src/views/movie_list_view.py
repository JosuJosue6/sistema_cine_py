from tkinter import Frame, Label, Scrollbar, StringVar, Entry, Button, END, messagebox, Toplevel, HORIZONTAL, Canvas, OptionMenu
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
        self.genre_var = StringVar(value="Género")
        self.classification_var = StringVar(value="Clasificación")
        self.language_var = StringVar(value="Idioma")
        self.create_widgets()

    # Método para crear los widgets de la interfaz
    def create_widgets(self):
        self.master.title("Cartelera de Películas")
        self.master.geometry("1200x800")  # Ajustar el tamaño de la ventana
        self.master.configure(bg="#f0f0f0")  # Fondo gris claro

        # Barra de navegación
        self.navbar = Frame(self, bg="#333", height=70)  # Fondo oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Arial", 24, "bold"), bg="#333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)  # Padding de 400px a la derecha

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/Screenshot 2024-07-14 232103.png"):  # Reemplaza con la ruta de tu imagen
            navbar_image = Image.open("src/assets/Screenshot 2024-07-14 232103.png")
            navbar_image = navbar_image.resize((50, 50), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS
            navbar_photo = ImageTk.PhotoImage(navbar_image)

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333")
            self.navbar_image_label.image = navbar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

        # Filtros en la navbar
        self.search_entry = Entry(self.navbar, width=30, font=("Arial", 14))  # Hacer la barra de búsqueda más grande
        self.search_entry.insert(0, "Buscar por nombre")  # Placeholder
        self.search_entry.bind("<FocusIn>", lambda event: self.search_entry.delete(0, END))
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<Return>", self.filter_movies)

        # Frame para los filtros
        self.filters_frame = Frame(self.navbar, bg="#333")
        self.filters_frame.pack(side="left", padx=10, pady=10)

        genres = ["Género", "Todos", "Acción", "Comedia", "Drama", "Terror"]  # Ejemplo de géneros
        classifications = ["Clasificación", "Todos", "G", "PG", "PG-13", "R"]  # Ejemplo de clasificaciones
        languages = ["Idioma", "Todos", "Español", "Inglés", "Francés"]  # Ejemplo de idiomas

        self.genre_menu = OptionMenu(self.filters_frame, self.genre_var, *genres, command=self.filter_movies)
        self.genre_menu.pack(side="left", padx=(40, 20), pady=10)  # Separar 40px de la imagen y 20px entre menús

        self.classification_menu = OptionMenu(self.filters_frame, self.classification_var, *classifications, command=self.filter_movies)
        self.classification_menu.pack(side="left", padx=20, pady=10)

        self.language_menu = OptionMenu(self.filters_frame, self.language_var, *languages, command=self.filter_movies)
        self.language_menu.pack(side="left", padx=20, pady=10)

        self.canvas_frame = Frame(self, bg="#f0f0f0")
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        self.canvas = Canvas(self.canvas_frame, bg="#f0f0f0")
        self.canvas.pack(side="top", fill="both", expand=True)

        self.scrollbar = Scrollbar(self.canvas_frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Título "Cartelera"
        self.cartelera_label = Label(self, text="Cartelera", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.cartelera_label.pack(pady=20)

        self.movie_listbox = Frame(self.canvas, bg="#f0f0f0")  # Fondo gris claro
        self.canvas.create_window((0, 0), window=self.movie_listbox, anchor="nw")

        self.details_label = Label(self, text="", wraplength=600, justify="left", font=("Arial", 12), bg="#f0f0f0")
        self.details_label.pack(pady=10)

        self.quit_button = Button(self, text="Salir", command=self.master.quit, font=("Arial", 12))
        self.quit_button.pack(pady=10)

        # Pie de página
        self.footer = Frame(self, bg="#333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2023 Sistema de Cine. Todos los derechos reservados.", font=("Arial", 10), bg="#333", fg="white")
        self.footer_label.pack(pady=10)

        self.load_movies()

    # Método para cargar las películas en la lista
    def load_movies(self):
        movies = self.movie_controller.fetch_movies()
        self.display_movies(movies)

    # Método para filtrar las películas por título, género, clasificación e idioma
    def filter_movies(self, event=None):
        query = self.search_entry.get().strip().lower()
        genre = self.genre_var.get()
        classification = self.classification_var.get()
        language = self.language_var.get()

        if genre == "Género":
            genre = None
        if classification == "Clasificación":
            classification = None
        if language == "Idioma":
            language = None
        if not query:
            query = None

        filtered_movies = self.movie_controller.filter_movies(genre, classification, language, query)
        self.display_movies(filtered_movies)

    # Método para mostrar las películas en la lista
    def display_movies(self, movies):
        for widget in self.movie_listbox.winfo_children():
            widget.destroy()

        if not movies:
            no_results_label = Label(self.movie_listbox, text="Lo siento, no hay resultados que coincidan con el criterio de búsqueda.", font=("Arial", 14), bg="#f0f0f0")
            no_results_label.pack(pady=20)
            return

        for index, movie in enumerate(movies):
            frame = Frame(self.movie_listbox, padx=10, pady=10, bd=2, relief="groove", bg="white")  # Fondo blanco para las tarjetas
            frame.grid(row=0, column=index, padx=25, pady=25)

            # Verificar si la imagen existe
            if os.path.exists(movie.image):
                # Cargar la imagen de la película
                image = Image.open(movie.image)
                image = image.resize((400, 600), Image.LANCZOS)  # Ajustar el tamaño de la imagen a 400px de ancho
                photo = ImageTk.PhotoImage(image)

                image_label = Label(frame, image=photo, bg="white")
                image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
                image_label.pack()

            title_label = Label(frame, text=movie.title, font=("Arial", 18, "bold"), fg="black", bg="white")  # Aumentar el tamaño de la fuente
            title_label.pack(pady=5)

            # Asociar el evento de clic para mostrar detalles
            frame.bind("<Button-1>", lambda e, m=movie: self.show_movie_details(m))

        self.movie_listbox.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # Método para mostrar los detalles de una película en una ventana emergente
    def show_movie_details(self, movie):
        popup = Toplevel(self)
        popup.title(movie.title)

        # Verificar si la imagen existe
        if os.path.exists(movie.image):
            # Cargar la imagen de la película
            image = Image.open(movie.image)
            image = image.resize((300, 450), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS
            photo = ImageTk.PhotoImage(image)

            image_label = Label(popup, image=photo)
            image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            image_label.pack(pady=10)

        details = f"Título: {movie.title}\nSinopsis: {movie.synopsis}\nGénero: {movie.genre}\nClasificación: {movie.classification}\nIdioma: {movie.language}\nDuración: {movie.duration} min"
        details_label = Label(popup, text=details, wraplength=400, justify="left", font=("Arial", 12))
        details_label.pack(pady=10)

        select_button = Button(popup, text="Seleccionar", command=lambda: self.open_ticket_selection(), font=("Arial", 12))
        select_button.pack(pady=5)

    # Método para abrir la ventana de selección de boletos
    def open_ticket_selection(self):
        ticket_selection_popup = Toplevel(self)
        ticket_selection_popup.title("Selección de Boletos")
        TicketSelectionView(ticket_selection_popup)

    # Método para seleccionar una película (puedes definir lo que hace)
    def select_movie(self, movie):
        messagebox.showinfo("Película seleccionada", f"Has seleccionado: {movie.title}")

class TicketSelectionView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Seleccione el tipo de boleto:").pack()

        ticket_options = ["Niño", "Adulto", "Adulto Mayor"]
        self.ticket_type = StringVar()
        OptionMenu(self, self.ticket_type, *ticket_options).pack()

        Label(self, text="Seleccione el método de pago:").pack()

        payment_options = ["Tarjeta", "Contado"]
        self.payment_method = StringVar()
        OptionMenu(self, self.payment_method, *payment_options).pack()

        Button(self, text="Confirmar selección", command=self.confirm_selection).pack()

    # Método para confirmar la selección del boleto
    def confirm_selection(self):
        selected_ticket = self.ticket_type.get()
        selected_payment = self.payment_method.get()
        messagebox.showinfo("Selección Confirmada", f"Tipo de boleto: {selected_ticket}\nMétodo de pago: {selected_payment}")