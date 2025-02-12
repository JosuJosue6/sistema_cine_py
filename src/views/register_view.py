from tkinter import Frame, Label, Entry, Button, messagebox, Toplevel
from controllers.user_controller import UserController
from PIL import Image, ImageTk, ImageDraw
import os

class RegisterUserView(Frame):
    def __init__(self, master, db_connection):
        super().__init__(master)
        self.master = master
        self.db_connection = db_connection
        self.user_controller = UserController(db_connection)
        self.init_ui()

    def init_ui(self):
        self.master.title("Registrar Usuario")
        self.master.state('zoomed')
        self.master.configure(bg="#f0f0f0")

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
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = Label(self.container, text="Registrar Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.name_label = Label(self.container, text="Nombre:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self.container, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.lastname_label = Label(self.container, text="Apellido:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.lastname_label.pack(pady=5)
        self.lastname_entry = Entry(self.container, font=("Arial", 12))
        self.lastname_entry.pack(pady=5)

        self.ci_label = Label(self.container, text="CI:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.ci_label.pack(pady=5)
        self.ci_entry = Entry(self.container, font=("Arial", 12))
        self.ci_entry.pack(pady=5)

        self.email_label = Label(self.container, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self.container, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        self.password_label = Label(self.container, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(self.container, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        self.confirm_password_label = Label(self.container, text="Confirmar Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = Entry(self.container, font=("Arial", 12), show="*")
        self.confirm_password_entry.pack(pady=5)

        self.register_button = Button(self.container, text="Registrar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.register_user)
        self.register_button.pack(pady=20)

        # Footer
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    def register_user(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        ci = self.ci_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not name or not lastname or not ci or not email or not password or not confirm_password:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        if password != confirm_password:
            messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
            return

        user_data = {
            'name': name,
            'lastname': lastname,
            'CI': ci,
            'email': email,
            'password': password
        }

        try:
            self.user_controller.create_user(user_data)
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario. Error: {e}")

    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.lastname_entry.delete(0, 'end')
        self.ci_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')

    def run(self):
        self.pack()
        self.master.mainloop()