from tkinter import Frame, Label, Button, messagebox, Toplevel, Canvas, Menu, Tk
from models.seat import Seat
from controllers.seat_controller import SeatController
from views.combo_selection_view import CombosSelectionView  # Asegúrate de importar la clase CombosSelectionView
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os
from views.user_detail_view import UserDetailView 

class SeatSelectionView(Frame):
    def __init__(self, master, movie, db_connection, ticket_count, subtotal, payment_method, email):
        super().__init__(master)
        self.master = master
        self.movie = movie
        self.email = email
        self.db_connection = db_connection
        self.seat_controller = SeatController(db_connection)
        self.ticket_count = ticket_count
        self.subtotal = subtotal  # Subtotal de los boletos
        self.payment_method = payment_method  # Método de pago
        self.selected_seats = []
        self.init_ui()

    def init_ui(self):

        self.master.title("Selecciona tus asientos")
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#f0f0f0")  # Fondo gris claro

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333", height=70)  # Fondo oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Arial", 30, "bold"), bg="#333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

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

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333")
            self.navbar_image_label.image = navbar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

            # Crear el menú desplegable
            self.navbar_menu = Menu(self.navbar, tearoff=0, bg="#333333", fg="white", font=("Helvetica", 12), activebackground="#1a1a1a", activeforeground="white")
            self.navbar_menu.add_command(label="Ver perfil", command=self.open_user_detail_view)
            self.navbar_menu.add_command(label="Cerrar sesión", command=self.logout)
            
            # Asociar el menú desplegable a la imagen
            self.navbar_image_label.bind("<Button-1>", self.show_navbar_menu)

        self.title_label = Label(self.master, text=f"Selecciona tus asientos para:\n {self.movie.title}", font=("Arial", 18, "bold"), bg="#FFD700", fg="#333",width=40, height=4)
        self.title_label.pack(pady=10)

        self.seat_frame = Frame(self.master, bg="#f0f0f0", bd=2, relief="solid", width=1000, height=800)
        self.seat_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.seat_buttons = self.create_seat_buttons()

        self.confirm_button = Button(self.master, text="Confirmar selección", command=self.confirm_selection, bg="#000000", fg="white", font=("Arial", 12, "bold"))
        self.confirm_button.place(relx=0.5, rely=0.75, anchor="center")

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    # Método para crear los botones de los asientos
    def create_seat_buttons(self):
        seats = self.seat_controller.get_seats()
        buttons = []
        row_mapping = {chr(i): i - 65 for i in range(65, 91)}  # Mapea 'A' a 0, 'B' a 1, etc.
        for seat in seats:
            #print(seat)
            row = row_mapping.get(seat.row, seat.row)  # Mapea la fila a un entero
            button_image = self.create_rounded_button_image("green" if seat.is_available() else "red")
            button = Button(self.seat_frame, image=button_image, text=f"{seat.row}{seat.number}", compound="center", fg="white",
                            command=lambda s=seat: self.toggle_seat(s))
            button.image = button_image  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            button.grid(row=row, column=seat.number, padx=5, pady=5)
            buttons.append(button)
        return buttons

    # Método para crear una imagen de botón redondeado
    def create_rounded_button_image(self, color, width=50, height=50, radius=10):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
        return ImageTk.PhotoImage(image)

    # Método para alternar la selección de un asiento
    def toggle_seat(self, seat):
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            self.update_button_color(seat, "green")
        else:
            if len(self.selected_seats) >= self.ticket_count:
                messagebox.showwarning("Advertencia", f"Solo puedes seleccionar {self.ticket_count} asientos.")
                return
            self.selected_seats.append(seat)
            self.update_button_color(seat, "yellow")

    # Método para actualizar el color de un botón de asiento
    def update_button_color(self, seat, color):
        for button in self.seat_buttons:
            if button.cget("text") == f"{seat.row}{seat.number}":
                button_image = self.create_rounded_button_image(color)
                button.config(image=button_image)
                button.image = button_image  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector

    # Método para confirmar la selección de asientos
    def confirm_selection(self):
        if len(self.selected_seats) != self.ticket_count:
            messagebox.showwarning("Advertencia", f"Debes seleccionar exactamente {self.ticket_count} asientos.")
            return

        # Actualizar el estado de los asientos seleccionados en la base de datos
        for seat in self.selected_seats:
            self.seat_controller.reserve_seat(seat.room, seat.row, seat.number)

        # Validar la selección de asientos
        messagebox.showinfo("Confirmación", f"Asientos seleccionados: {', '.join([f'{s.row}{s.number}' for s in self.selected_seats])}")

        # Abrir la vista de selección de combos
        self.open_combos_selection()

    # Método para abrir la vista de selección de combos
    def open_combos_selection(self):
        self.master.withdraw()  # Ocultar la ventana de SeatSelectionView
        combos_selection_window = Toplevel(self.master)
        combos_selection_view = CombosSelectionView(combos_selection_window, self.movie, self.selected_seats, self.db_connection, self.subtotal, self.payment_method, self.email)
        combos_selection_view.pack()
        combos_selection_window.protocol("WM_DELETE_WINDOW", lambda: (self.master.deiconify(), combos_selection_window.destroy()))  # Mostrar la ventana principal cuando se cierre la nueva ventana

    def show_navbar_menu(self, event):
            self.navbar_menu.post(event.x_root, event.y_root)

    def open_user_detail_view(self):
        user_detail_window = Toplevel(self.master)
        user_detail_view = UserDetailView(user_detail_window, self.db_connection, self.email)
        user_detail_view.pack(fill="both", expand=True)
        user_detail_window.mainloop()

    def logout(self):
        from views.login_view import LoginView
        self.master.destroy()
        login_window = Tk()
        login_view = LoginView(login_window, self.db_connection)
        login_view.pack(fill="both", expand=True)
        login_window.mainloop()   
    def run(self):
        self.pack()
        self.master.mainloop()

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