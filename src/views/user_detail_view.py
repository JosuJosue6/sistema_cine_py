from tkinter import Frame, Label, Entry, Button, messagebox, Toplevel
from controllers.user_controller import UserController
from PIL import Image, ImageTk, ImageDraw
import os

class UserDetailView(Frame):
    def __init__(self, master, db_connection, user_email):
        super().__init__(master)
        self.master = master
        self.db_connection = db_connection
        self.user_controller = UserController(db_connection)
        self.user_id = self.user_controller.get_id_by_email(user_email)
        self.user = self.user_controller.get_user(self.user_id)
        if self.user is None:
            messagebox.showerror("Error", "Usuario no encontrado.")
            self.master.destroy()
        else:
            self.bg_photo = None
            self.init_ui()

    def init_ui(self):
        self.master.title("Detalles del Usuario")
        self.master.state('zoomed')
        self.master.configure(bg="#000000")

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

        # Navbar
        self.navbar = Frame(self.master, bg="#333333", height=70)
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

        if os.path.exists("src/assets/image/image.jpg"):
            navbar_image = Image.open("src/assets/image/image.jpg")
            navbar_image = navbar_image.resize((50, 50), Image.LANCZOS)

            mask = Image.new("L", navbar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + navbar_image.size, fill=255)
            navbar_image.putalpha(mask)

            navbar_photo = ImageTk.PhotoImage(navbar_image)

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333333")
            self.navbar_image_label.image = navbar_photo
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

        # Main container with border
        self.container = Frame(self.master, bg="#f0f0f0", bd=2, relief="solid", highlightbackground="black", highlightthickness=2)
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=600)

        self.title_label = Label(self.container, text="Detalles del Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.name_label = Label(self.container, text="Nombre:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.name_label.pack(pady=10)
        self.name_entry = Entry(self.container, font=("Arial", 12))
        self.name_entry.pack(pady=10)
        self.name_entry.insert(0, self.user.name)

        self.lastname_label = Label(self.container, text="Apellido:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.lastname_label.pack(pady=10)
        self.lastname_entry = Entry(self.container, font=("Arial", 12))
        self.lastname_entry.pack(pady=10)
        self.lastname_entry.insert(0, self.user.lastname)

        self.ci_label = Label(self.container, text="CI:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.ci_label.pack(pady=10)
        self.ci_entry = Entry(self.container, font=("Arial", 12))
        self.ci_entry.pack(pady=10)
        self.ci_entry.insert(0, self.user.CI)

        self.email_label = Label(self.container, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.email_label.pack(pady=10)
        self.email_entry = Entry(self.container, font=("Arial", 12))
        self.email_entry.pack(pady=10)
        self.email_entry.insert(0, self.user.email)

        self.password_label = Label(self.container, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(self.container, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=10)
        self.password_entry.insert(0, self.user.password)

        button_width = 20  # Ancho de los botones

        self.update_button = Button(self.container, text="Actualizar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.update_user, width=button_width)
        self.update_button.pack(pady=10)

        self.delete_button = Button(self.container, text="Eliminar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.delete_user, width=button_width)
        self.delete_button.pack(pady=10)

        # Footer
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    def load_background_image(self):
        if os.path.exists("src/assets/Test.jpg"):  # Reemplaza con la ruta de tu imagen de fondo
            bg_image = Image.open("src/assets/Test.jpg")
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
            bg_image = Image.open("src/assets/Test.jpg")
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label.config(image=self.bg_photo)

    def update_user(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        ci = self.ci_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not lastname or not ci or not email or not password:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        user_data = {
            'name': name,
            'lastname': lastname,
            'CI': ci,
            'email': email,
            'password': password
        }

        try:
            self.user_controller.update_user(self.user_id, user_data)
            messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el usuario. Error: {e}")

    def delete_user(self):
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirm:
            try:
                self.user_controller.delete_user(self.user_id)
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                self.open_login_view()
                self.master.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el usuario. Error: {e}")

    def open_login_view(self):
        from views.login_view import LoginView  # Importación diferida para evitar importación circular
        login_window = Toplevel(self.master)
        login_view = LoginView(login_window, self.db_connection)
        login_view.pack(fill="both", expand=True)
        login_window.mainloop()

    def run(self):
        self.pack()
        self.master.mainloop()