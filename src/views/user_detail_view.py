from tkinter import Frame, Label, Entry, Button, messagebox, Toplevel
from controllers.user_controller import UserController

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
            self.init_ui()

    def init_ui(self):
        self.master.title("Detalles del Usuario")
        self.master.geometry("400x550")
        self.master.configure(bg="#f0f0f0")

        self.title_label = Label(self, text="Detalles del Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.name_label = Label(self, text="Nombre:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self, font=("Arial", 12))
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, self.user.name)

        self.lastname_label = Label(self, text="Apellido:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.lastname_label.pack(pady=5)
        self.lastname_entry = Entry(self, font=("Arial", 12))
        self.lastname_entry.pack(pady=5)
        self.lastname_entry.insert(0, self.user.lastname)

        self.ci_label = Label(self, text="CI:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.ci_label.pack(pady=5)
        self.ci_entry = Entry(self, font=("Arial", 12))
        self.ci_entry.pack(pady=5)
        self.ci_entry.insert(0, self.user.CI)

        self.email_label = Label(self, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, self.user.email)

        self.password_label = Label(self, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, self.user.password)

        self.update_button = Button(self, text="Actualizar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.update_user)
        self.update_button.pack(pady=10)

        self.delete_button = Button(self, text="Eliminar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.delete_user)
        self.delete_button.pack(pady=10)

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

