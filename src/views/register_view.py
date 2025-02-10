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
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f0f0")

        self.title_label = Label(self, text="Registrar Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.name_label = Label(self, text="Nombre:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.email_label = Label(self, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        self.password_label = Label(self, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        self.register_button = Button(self, text="Registrar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.register_user)
        self.register_button.pack(pady=20)

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        user_data = {
            'name': name,
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
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def run(self):
        self.pack()
        self.master.mainloop()

# Ejemplo de uso
if __name__ == "__main__":
    from tkinter import Tk
    from db_connection import DBConnection  # Asegúrate de tener una clase DBConnection para manejar la conexión a la base de datos

    root = Tk()
    db_connection = DBConnection()  # Inicializa tu conexión a la base de datos
    app = RegisterUserView(root, db_connection)
    app.run()