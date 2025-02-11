from tkinter import Frame, Label, Entry, Button, messagebox
from controllers.user_controller import UserController

class RegisterUserView(Frame):
    def __init__(self, master, db_connection):
        super().__init__(master)
        self.master = master
        self.db_connection = db_connection
        self.user_controller = UserController(db_connection)
        self.init_ui()

    def init_ui(self):
        self.master.title("Registrar Usuario")
        self.master.geometry("400x550")
        self.master.configure(bg="#f0f0f0")

        self.title_label = Label(self, text="Registrar Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.name_label = Label(self, text="Nombre:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.lastname_label = Label(self, text="Apellido:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.lastname_label.pack(pady=5)
        self.lastname_entry = Entry(self, font=("Arial", 12))
        self.lastname_entry.pack(pady=5)

        self.ci_label = Label(self, text="CI:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.ci_label.pack(pady=5)
        self.ci_entry = Entry(self, font=("Arial", 12))
        self.ci_entry.pack(pady=5)

        self.email_label = Label(self, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        self.password_label = Label(self, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        self.confirm_password_label = Label(self, text="Confirmar Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = Entry(self, font=("Arial", 12), show="*")
        self.confirm_password_entry.pack(pady=5)

        self.register_button = Button(self, text="Registrar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.register_user)
        self.register_button.pack(pady=20)

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