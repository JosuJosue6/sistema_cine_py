from tkinter import Tk, Frame, Label, Entry, Button, messagebox, Toplevel
from PIL import Image, ImageTk, ImageDraw
import os
from controllers.user_controller import UserController
from views.movie_list_view import MovieListView  # Importa la clase MovieListView
from views.register_view import RegisterUserView  # Importa la clase RegisterUserView

class LoginView(Frame):
    def __init__(self, master, db_connection):
        super().__init__(master)
        self.master = master
        self.db_connection = db_connection
        self.email = None
        self.user_controller = UserController(db_connection)
        self.bg_photo = None
        #self.bg_image = "src/assets/cine1.jpeg" 
        #self.bg_image = "src/assets/cine2.jpeg" 
        #self.bg_image = "src/assets/cine3.jpeg" 
        #self.bg_image = "src/assets/cine4.jpeg" 
        self.bg_image = "src/assets/Test.jpg" 
        self.ventana()
         # Ruta de la imagen de fondo

    def ventana(self):
        self.master.title("Inicio de Sesión")
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#000000") 

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

        # Contenedor central con bordes redondeados
        self.container = Frame(self.master, bg="#333333", bd=2, relief="solid")
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=600)

        # Frame dentro del contenedor para contener los widgets
        self.inner_frame = Frame(self.container, bg="#000000")
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=580)

        # Espacio para la imagen redondeada
        if os.path.exists("src/assets/image/image.jpg"):  # Reemplaza con la ruta de tu imagen
            avatar_image = Image.open("src/assets/image/image.jpg")
            avatar_image = avatar_image.resize((100, 100), Image.LANCZOS)

            # Crear una máscara circular
            mask = Image.new("L", avatar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + avatar_image.size, fill=255)
            avatar_image.putalpha(mask)

            avatar_photo = ImageTk.PhotoImage(avatar_image)

            self.avatar_label = Label(self.inner_frame, image=avatar_photo, bg="#000000")
            self.avatar_label.image = avatar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            self.avatar_label.pack(pady=(20, 10))

        self.title_label = Label(self.inner_frame, text="Inicio de Sesión", font=("Arial", 24, "bold"), bg="#000000", fg="white")
        self.title_label.pack(pady=10)

        self.email_label = Label(self.inner_frame, text="Correo Electrónico:", font=("Arial", 14), bg="#000000", fg="white")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self.inner_frame, font=("Arial", 14), width=30)
        self.email_entry.pack(pady=5)

        self.password_label = Label(self.inner_frame, text="Contraseña:", font=("Arial", 14), bg="#000000", fg="white")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(self.inner_frame, font=("Arial", 14), width=30, show="*")
        self.password_entry.pack(pady=5)

        button_width = 20  # Ancho de los botones

        self.login_button = Button(self.inner_frame, text="Iniciar Sesión", command=self.login, font=("Arial", 14, "bold"), bg="#F5A900", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2, width=button_width)
        self.login_button.pack(pady=20)

        self.register_button = Button(self.inner_frame, text="Registrar", command=self.open_register_view, font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2, width=button_width, highlightbackground="#F5A900", highlightthickness=2)
        self.register_button.pack(pady=10)

        # Vincular la tecla "Enter" al método login
        self.master.bind('<Return>', lambda event: self.login())

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    def load_background_image(self):
        if os.path.exists(self.bg_image): 
            bg_image = Image.open(self.bg_image)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = Label(self.master, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def resize_background(self, event):
        if self.bg_photo:
            screen_width = self.master.winfo_width()
            screen_height = self.master.winfo_height()
            bg_image = Image.open(self.bg_image)
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label.config(image=self.bg_photo)

    def login(self):
        self.email = self.email_entry.get()
        password = self.password_entry.get()
        # Validar las credenciales del usuario
        user = self.user_controller.authenticate_user(self.email, password)
        if user:
            messagebox.showinfo("Inicio de Sesión", f"Bienvenido !")
            self.open_movie_list_view()
        else:
            messagebox.showerror("Error", "Correo electrónico o contraseña incorrectos.")

    def open_movie_list_view(self):
        # Destruir la vista actual antes de abrir la nueva vista
        self.master.destroy()
        movie_list_window = Tk()
        movie_list_view = MovieListView(movie_list_window, self.db_connection, self.email)
        movie_list_view.pack(fill="both", expand=True)
        movie_list_window.mainloop()

    def open_register_view(self):
        # Abrir la vista de registro de usuario
        register_window = Toplevel(self.master)
        register_view = RegisterUserView(register_window, self.db_connection)
        register_view.pack(fill="both", expand=True)
        register_window.mainloop()
