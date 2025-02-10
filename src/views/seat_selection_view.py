from tkinter import Frame, Label, Button, messagebox, Toplevel, Canvas
from models.seat import Seat
from controllers.seat_controller import SeatController
from views.combo_selection_view import CombosSelectionView  # Asegúrate de importar la clase CombosSelectionView
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os

class SeatSelectionView(Frame):
    def __init__(self, master, movie, db_connection, ticket_count, subtotal, payment_method):
        super().__init__(master)
        self.master = master
        self.movie = movie
        self.db_connection = db_connection
        self.seat_controller = SeatController(db_connection)
        self.ticket_count = ticket_count
        self.subtotal = subtotal  # Subtotal de los boletos
        self.payment_method = payment_method  # Método de pago
        self.selected_seats = []
        self.init_ui()

    def init_ui(self):
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#f0f0f0")  # Fondo gris claro

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333", height=70)  # Fondo oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Arial", 30, "bold"), bg="#333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/movies/movie1.jpg"):  
            navbar_image = Image.open("src/assets/movies/movie1.jpg")
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

        self.title_label = Label(self, text=f"Selecciona tus asientos para: {self.movie.title}", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.seat_frame = Frame(self, bg="#f0f0f0")
        self.seat_frame.pack(pady=10)

        self.seat_buttons = self.create_seat_buttons()

        self.confirm_button = Button(self, text="Confirmar selección", command=self.confirm_selection, bg="#000000", fg="white", font=("Arial", 12, "bold"))
        self.confirm_button.pack(pady=10)

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
            print(seat)
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

        # Validar la selección de asientos
        messagebox.showinfo("Confirmación", f"Asientos seleccionados: {', '.join([f'{s.row}{s.number}' for s in self.selected_seats])}")

        # Abrir la vista de selección de combos
        self.open_combos_selection()

    # Método para abrir la vista de selección de combos
    def open_combos_selection(self):
        self.master.withdraw()  # Ocultar la ventana de SeatSelectionView
        combos_selection_window = Toplevel(self.master)
        combos_selection_view = CombosSelectionView(combos_selection_window, self.movie, self.selected_seats, self.db_connection, self.subtotal, self.payment_method)
        combos_selection_view.pack()
        combos_selection_window.protocol("WM_DELETE_WINDOW", lambda: (self.master.deiconify(), combos_selection_window.destroy()))  # Mostrar la ventana principal cuando se cierre la nueva ventana

    def run(self):
        self.pack()
        self.master.mainloop()