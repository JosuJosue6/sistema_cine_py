from tkinter import Tk, LEFT, RIGHT, Frame, Label, Scrollbar, StringVar, Entry, Button, END, messagebox, Toplevel, HORIZONTAL, Canvas, OptionMenu, ttk
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
from controllers.movie_controller import MovieController
import os
from views.ticket_selection_view import TicketSelectionView

class MovieListView(Frame):
    def __init__(self, master, db_connection, email):
        super().__init__(master)
        self.master = master
        self.email = email
        self.movie_controller = MovieController(db_connection)
        self.selected_movie = StringVar()
        self.genre_var = StringVar(value="Género")
        self.classification_var = StringVar(value="Clasificación")
        self.language_var = StringVar(value="Idioma")
        self.create_widgets()

    # Método para crear los widgets de la interfaz
    def create_widgets(self):
        self.master.title("Cartelera de Películas")

        # Maximizar la ventana
        self.master.state('zoomed')
        
        self.master.configure(bg="#000000")  # Fondo negro

        # Barra de navegación
        self.navbar = Frame(self, bg="#333333", height=100)  # Fondo gris oscuro y altura aumentada
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 30, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 200), pady=10)  # Mover más a la izquierda

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/image/image.jpg"):  
            navbar_image = Image.open("src/assets/image/image.jpg")
            navbar_image = navbar_image.resize((60, 60), Image.LANCZOS) 

            # Crear una máscara circular
            mask = Image.new("L", navbar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + navbar_image.size, fill=255)
            navbar_image.putalpha(mask)

            navbar_photo = ImageTk.PhotoImage(navbar_image)

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333333")
            self.navbar_image_label.image = navbar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

        # Título "Cartelera"
        self.cartelera_label = Label(self, text="Cartelera", font=("Helvetica", 24, "bold"), fg="black")
        self.cartelera_label.pack(pady=(10, 5))  # Reducir el padding superior a 10 y el inferior a 5

        # Barra de búsqueda
        self.search_entry = Entry(self.navbar, width=30, font=("Helvetica", 14), fg="#999999")  # Hacer la barra de búsqueda más grande y cambiar el color del placeholder
        self.search_entry.insert(0, "Buscar por nombre")  # Placeholder
        self.search_entry.bind("<FocusIn>", lambda event: self.search_entry.delete(0, END))
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<Return>", self.filter_movies)
        self.search_entry.config(highlightbackground="#333333", highlightcolor="#333333", highlightthickness=1, bd=0, relief="solid")
        self.search_entry.bind("<FocusOut>", self.on_focus_out)
        self.search_entry.config(relief="solid", bd=1, highlightthickness=0, highlightbackground="#333333")
        self.search_entry.config(insertbackground="black", insertwidth=2)
        self.search_entry.config(borderwidth=2, relief="groove")

        # Estilo para las listas desplegables
        self.option_menu_style = {
            "bg": "#333333",
            "fg": "white",
            "activebackground": "#1a1a1a",
            "activeforeground": "white",
            "font": ("Helvetica", 12),
            "width": 15  # Fijar el ancho de los menús desplegables
        }

        # Frame para los filtros
        self.filters_frame = Frame(self.navbar, bg="#333333")
        self.filters_frame.pack(side="left", padx=10, pady=10)  # Mover más a la izquierda

        genres = ["Género", "Todos", "Acción","Animación", "Aventura", "Comedia", "Documental","Horror", "Terror", "Thriller"]  # Ejemplo de géneros
        classifications = ["Clasificación", "Todos", "12+ años", "15+ años"]  # Ejemplo de clasificaciones
        languages = ["Idioma", "Todos", "Español", "Inglés"]  # Ejemplo de idiomas

        self.genre_menu = OptionMenu(self.filters_frame, self.genre_var, *genres, command=self.filter_movies)
        self.genre_menu.config(**self.option_menu_style)
        self.genre_menu["menu"].config(bg="#333333", fg="white", font=("Helvetica", 12), activebackground="#1a1a1a", activeforeground="white")  # Cambiar el color de fondo y texto de la lista desplegable
        self.genre_menu.pack(side="left", padx=(20, 10), pady=10)  # Separar 20px de la barra de búsqueda y 10px entre menús

        self.classification_menu = OptionMenu(self.filters_frame, self.classification_var, *classifications, command=self.filter_movies)
        self.classification_menu.config(**self.option_menu_style)
        self.classification_menu["menu"].config(bg="#333333", fg="white", font=("Helvetica", 12), activebackground="#1a1a1a", activeforeground="white")  # Cambiar el color de fondo y texto de la lista desplegable
        self.classification_menu.pack(side="left", padx=10, pady=10)

        self.language_menu = OptionMenu(self.filters_frame, self.language_var, *languages, command=self.filter_movies)
        self.language_menu.config(**self.option_menu_style)
        self.language_menu["menu"].config(bg="#333333", fg="white", font=("Helvetica", 12), activebackground="#1a1a1a", activeforeground="white")  # Cambiar el color de fondo y texto de la lista desplegable
        self.language_menu.pack(side="left", padx=10, pady=10)

        # Aplicar estilo de subrayado y cambio de color al pasar el cursor sobre las listas desplegables
        self.apply_hover_effect(self.genre_menu)
        self.apply_hover_effect(self.classification_menu)
        self.apply_hover_effect(self.language_menu)

        self.canvas_frame = Frame(self, bg="#000000")
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        self.canvas = Canvas(self.canvas_frame, bg="#000000")
        self.canvas.pack(side="top", fill="both", expand=True)

         # Crear un estilo personalizado para la barra de desplazamiento
        style = ttk.Style()
        style.configure("TScrollbar", troughcolor="#333333", background="#666666", darkcolor="#444444", lightcolor="#444444", arrowcolor="#ffffff")

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient=HORIZONTAL, command=self.canvas.xview, style="TScrollbar")
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.movie_listbox = Frame(self.canvas, bg="#000000")  # Fondo negro
        self.canvas.create_window((0, 0), window=self.movie_listbox, anchor="nw")

        self.details_label = Label(self, text="", wraplength=600, justify="left", font=("Helvetica", 12), bg="#000000", fg="white")
        self.details_label.pack(pady=10)

        self.quit_button = Button(self, text="Salir", command=self.master.quit, font=("Helvetica", 16, "bold"), bg="#1a1a1a", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        self.quit_button.pack(pady=(5, 10))  # Reducir el padding superior a 5 y el inferior a 10
        #self.quit_button.config(width=20, height=2, borderwidth=2, relief="groove", highlightbackground="#555555", highlightcolor="#555555", highlightthickness=2)

        # Pie de página
        self.footer = Frame(self, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

        self.load_movies()

    def apply_hover_effect(self, widget):
        def on_enter(event):
            widget.config(fg="#FFD700", underline=True)

        def on_leave(event):
            widget.config(fg="white", underline=False)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def on_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar por nombre")
            self.search_entry.config(fg="#999999")

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
        title = self.search_entry.get()

        if genre == "Género":
            genre = None
        if classification == "Clasificación":
            classification = None
        if language == "Idioma":
            language = None
        if not query:
            query = None
        if genre == "Todos":
            genre = None
        if classification == "Todos":
            classification = None
        if language == "Todos":
            language = None
        if title == "Buscar por nombre":
            query = None

        filtered_movies = self.movie_controller.filter_movies(genre, classification, language, query)
        self.display_movies(filtered_movies)

    # Método para mostrar las películas en la lista
    def display_movies(self, movies):
        for widget in self.movie_listbox.winfo_children():
            widget.destroy()

        if not movies:
            no_results_label = Label(self.movie_listbox, text="Lo siento, no hay resultados que coincidan con el criterio de búsqueda.", font=("Helvetica", 14), bg="#000000", fg="white")
            no_results_label.pack(pady=20)
            return

        for index, movie in enumerate(movies):
            frame = Frame(self.movie_listbox, padx=10, pady=10, bd=2, relief="groove", bg="#1a1a1a")  # Fondo gris oscuro para las tarjetas
            frame.grid(row=0, column=index, padx=25, pady=25)

            # Verificar si la imagen existe
            if os.path.exists(movie.image):
                # Cargar la imagen de la película
                image = Image.open(movie.image)
                image = image.resize((300, 400), Image.LANCZOS)  # Ajustar el tamaño de la imagen a 300px de ancho
                photo = ImageTk.PhotoImage(image)

                image_label = Label(frame, image=photo, bg="#1a1a1a")
                image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
                image_label.pack()

                # Asociar el evento de clic para mostrar detalles
                image_label.bind("<Button-1>", lambda e, m=movie: self.show_movie_details(m))

            title_label = Label(frame, text=movie.title, font=("Helvetica", 18, "bold"), fg="white", bg="#1a1a1a")  # Aumentar el tamaño de la fuente
            title_label.pack(pady=5)

            # Asociar el evento de clic para mostrar detalles
            title_label.bind("<Button-1>", lambda e, m=movie: self.show_movie_details(m))

        self.movie_listbox.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # Método para mostrar los detalles de una película en una ventana emergente
    def show_movie_details(self, movie):
        popup = Toplevel(self)
        popup.title(movie.title)

        # Maximizar la ventana
        popup.state('zoomed')

        # Barra de navegación para la ventana emergente
        navbar = Frame(popup, bg="#333333", height=70)  # Fondo gris oscuro
        navbar.pack(side="top", fill="x")
        navbar_label = Label(navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        navbar_label.pack(side="left", padx=(10, 400), pady=10)

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/image/image.jpg"):  # Reemplaza con la ruta de tu imagen
            navbar_image = Image.open("src/assets/image/image.jpg")
            navbar_image = navbar_image.resize((50, 50), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS

            # Crear una máscara circular
            mask = Image.new("L", navbar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + navbar_image.size, fill=255)
            navbar_image.putalpha(mask)

            navbar_photo = ImageTk.PhotoImage(navbar_image)

            navbar_image_label = Label(navbar, image=navbar_photo, bg="#333333")
            navbar_image_label.image = navbar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            navbar_image_label.pack(side="right", padx=10, pady=10)

        # Frame para contener la imagen y los detalles
        content_frame = Frame(popup, bd=2, highlightbackground="black", highlightthickness=2, width=500, height=500)
        content_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Verificar si la imagen existe
        if os.path.exists(movie.image):
            # Cargar la imagen de la película
            image = Image.open(movie.image)
            image = image.resize((300, 450), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS
            photo = ImageTk.PhotoImage(image)

            image_label = Label(content_frame, image=photo)
            image_label.image = photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            image_label.pack(side="left", padx=20, pady=5)  # Mayor padding horizontal, menor padding vertical

        # Frame para los detalles de la película
        details_frame = Frame(content_frame)
        details_frame.pack(side="left", padx=100, pady=100, fill="both", expand=True)

        title_label = Label(details_frame, text=movie.title, font=("Helvetica", 18, "bold"), wraplength=400, justify="left")
        title_label.pack(anchor="w", pady=10)  # Alinear a la izquierda y agregar padding vertical

        details = f"Sinopsis: {movie.synopsis}\n\nGénero: {movie.genre}\nClasificación: {movie.classification}\nIdioma: {movie.language}\nDuración: {movie.duration} min"
        details_label = Label(details_frame, text=details, wraplength=400, justify="left", font=("Helvetica", 12))
        details_label.pack(anchor="w", pady=10)  # Alinear a la izquierda y agregar padding vertical

        # Frame para contener los botones
        button_frame = Frame(popup)
        button_frame.pack(pady=10)  # Asegurar que el frame de botones esté en la parte inferior

        # Botón para cerrar la ventana emergente
        close_button = Button(button_frame, text="Regresar", command=popup.destroy, font=("Helvetica", 14, "bold"), bg="#1a1a1a", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        close_button.pack(side=LEFT, padx=10)
        close_button.config(width=15, height=2, borderwidth=2, relief="groove", highlightbackground="#555555", highlightcolor="#555555", highlightthickness=2)

        # Botón para ver más detalles
        more_details_button = Button(button_frame, text="Seleccionar", command=lambda: self.open_ticket_selection(movie), font=("Helvetica", 14, "bold"), bg="#1a1a1a", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        more_details_button.pack(side=RIGHT, padx=10)
        more_details_button.config(width=15, height=2, borderwidth=2, relief="groove", highlightbackground="#555555", highlightcolor="#555555", highlightthickness=2)

        # Pie de página
        footer = Frame(popup, bg="#333333", height=50)
        footer.pack(side="bottom", fill="x")

        footer_label = Label(footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        footer_label.pack(pady=10)

    # Método para abrir la ventana de selección de boletos
    def open_ticket_selection(self, movie):
        
        self.master.destroy()  # Cerrar la ventana de MovieListView
        ticket_selection_window = Tk()
        ticket_selection_view = TicketSelectionView(ticket_selection_window, self.movie_controller.db_connection, movie,self.email)
        ticket_selection_view.pack(fill="both", expand=True)
        ticket_selection_window.mainloop()