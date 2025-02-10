from tkinter import Frame, Label, Button, StringVar, OptionMenu, messagebox, Toplevel, Entry, IntVar
from views.seat_selection_view import SeatSelectionView
from models.seat import Seat
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os
from controllers.ticket_controller import TicketController

class TicketSelectionView(Frame):
    def __init__(self, master, db_connection, movie):
        super().__init__(master)
        self.master = master
        self.db_connection = db_connection
        self.movie = movie
        self.ticket_controller = TicketController(db_connection)
        self.ticket_type_vars = []
        self.ticket_count = None
        self.subtotal = 0  # Variable para almacenar el subtotal
        self.payment_method = StringVar()  # Variable para almacenar el método de pago
        self.init_ui()

    # Método para inicializar la interfaz
    def init_ui(self):

        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#ffffff")  # Fondo blanco

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=100)  # Fondo gris claro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 30, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 200), pady=10)

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

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333333")
            self.navbar_image_label.image = navbar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

        self.ticket_count_var = IntVar()

        # Contenedor central con borde negro
        self.container = Frame(self, bg="#ffffff", bd=2, relief="solid", highlightbackground="black", highlightthickness=2)
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=600, height=600)

        Label(self.container, text=f"Seleccionar boletos para: {self.movie.title}", font=("Arial", 14), bg="#ffffff", fg="black").pack(pady=10)
        Label(self.container, text=f"Género: {self.movie.genre}", font=("Arial", 12), bg="#ffffff", fg="black").pack(pady=5)
        Label(self.container, text=f"Clasificación: {self.movie.classification}", font=("Arial", 12), bg="#ffffff", fg="black").pack(pady=5)
        Label(self.container, text=f"Duración: {self.movie.duration} min", font=("Arial", 12), bg="#ffffff", fg="black").pack(pady=5)

        Label(self.container, text="Ingrese el número de boletos:", bg="#ffffff", fg="black").pack(pady=5)
        ticket_count_options = list(range(1, 11))  # Opciones de 1 a 10 boletos
        OptionMenu(self.container, self.ticket_count_var, *ticket_count_options).pack(pady=5)

        Button(self.container, text="Confirmar número de boletos", command=self.confirm_ticket_count, font=("Arial", 12, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2).pack(pady=10)

        self.ticket_type_frame = Frame(self.container, bg="#ffffff")
        self.ticket_type_frame.pack(pady=10)

        Label(self.container, text="Seleccione el método de pago:", bg="#ffffff", fg="black").pack(pady=5)
        payment_options = ["Tarjeta", "Contado"]
        OptionMenu(self.container, self.payment_method, *payment_options).pack()

        self.subtotal_label = Label(self.container, text="Subtotal: N/A", bg="#ffffff", fg="black")
        self.subtotal_label.pack(pady=10)

        Button(self.container, text="Confirmar selección", command=self.confirm_selection, font=("Arial", 12, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2).pack(pady=10)

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    # Método para confirmar el número de boletos
    def confirm_ticket_count(self):
        try:
            self.ticket_count = self.ticket_count_var.get()
            if self.ticket_count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un número válido de boletos.")
            return

        # Limpiar el frame de tipos de boletos
        for widget in self.ticket_type_frame.winfo_children():
            widget.destroy()

        self.ticket_type_vars = []
        self.price_labels = []
        self.ticket_prices = self.ticket_controller.get_ticket_types()
        ticket_options = ["Niño", "Adulto", "Adulto Mayor"]

        for i in range(self.ticket_count):
            frame = Frame(self.ticket_type_frame, bg="#ffffff")
            frame.pack(side="left", padx=10, pady=5)

            Label(frame, text=f"Tipo de boleto {i + 1}:", bg="#ffffff", fg="black").pack(pady=5)
            ticket_type_var = StringVar()
            self.ticket_type_vars.append(ticket_type_var)
            OptionMenu(frame, ticket_type_var, *ticket_options).pack(pady=5)

            price_label = Label(frame, text="Precio: N/A", bg="#ffffff", fg="black")
            price_label.pack(pady=5)
            self.price_labels.append(price_label)

            ticket_type_var.trace("w", lambda *args, var=ticket_type_var, label=price_label: self.update_ticket_price(var, label))

    def update_ticket_price(self, ticket_type_var, label):
        ticket_type = ticket_type_var.get()
        price = next((item['price'] for item in self.ticket_prices if item['type'] == ticket_type), "N/A")
        label.config(text=f"Precio: {price}")
        self.update_subtotal()

    def update_subtotal(self):
        self.subtotal = 0  # Reiniciar el subtotal
        for var in self.ticket_type_vars:
            ticket_type = var.get()
            price = next((item['price'] for item in self.ticket_prices if item['type'] == ticket_type), 0)
            self.subtotal += price
        self.subtotal_label.config(text=f"Subtotal: {self.subtotal}")

    # Método para confirmar la selección del boleto
    def confirm_selection(self):
        ticket_types = [var.get() for var in self.ticket_type_vars]
        payment = self.payment_method.get()

        if not all(ticket_types) or not payment:
            messagebox.showwarning("Advertencia", "Por favor, seleccione todos los tipos de boletos y el método de pago.")
            return

        # Aquí se puede agregar la lógica para calcular el precio y aplicar promociones
        messagebox.showinfo("Confirmación", f"Boletos: {', '.join(ticket_types)}\nMétodo de pago: {payment}\nPelícula: {self.movie.title}\nSubtotal: {self.subtotal}")

        # Abrir la vista de selección de asientos
        self.open_seat_selection()

    # Método para abrir la vista de selección de asientos
    def open_seat_selection(self):
        self.master.withdraw()  # Ocultar la ventana de TicketSelectionView
        seat_selection_window = Toplevel(self.master)
        seat_selection_view = SeatSelectionView(seat_selection_window, self.movie, self.db_connection, self.ticket_count, self.subtotal, self.payment_method.get())
        seat_selection_view.pack()
        seat_selection_window.protocol("WM_DELETE_WINDOW", self.master.destroy)  # Destruir la ventana principal cuando se cierre la nueva ventana

    def run(self):
        self.pack()
        self.master.mainloop()