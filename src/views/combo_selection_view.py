from tkinter import Frame, Label, Button, Listbox, StringVar, Entry, messagebox, Toplevel, Radiobutton, IntVar
from views.promotions_view import PromotionsView  # Asegúrate de importar la clase PromotionsView
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os
from controllers.combo_controller import ComboController

class CombosSelectionView(Frame):
    def __init__(self, master, movie, selected_seats, db_connection, subtotal, payment_method, email):
        super().__init__(master)
        self.master = master
        self.movie = movie
        self.email = email
        self.selected_seats = selected_seats
        self.db_connection = db_connection
        self.subtotal = subtotal  # Subtotal de los boletos
        self.payment_method = payment_method  # Método de pago
        self.combo_controller = ComboController(db_connection)
        self.combos = self.load_combos()
        self.selected_combos = []
        self.total_price = 0.0

        self.init_ui()

    # Método para inicializar la interfaz
    def init_ui(self):
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#000000")  # Fondo negro

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=100)  # Fondo gris oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 30, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 200), pady=10)

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/movies/movie1.jpg"):  # Reemplaza con la ruta de tu imagen
            navbar_image = Image.open("src/assets/movies/movie1.jpg")
            navbar_image = navbar_image.resize((60, 60), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS
            
            # Crear una máscara circular
            mask = Image.new("L", navbar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + navbar_image.size, fill=255)
            navbar_image.putalpha(mask)

            navbar_photo = ImageTk.PhotoImage(navbar_image)

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333333")
            self.navbar_image_label.image = navbar_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

        self.title_label = Label(self, text=f"Selecciona tus combos para: {self.movie.title}", font=("Helvetica", 18, "bold"), bg="#000000", fg="white")
        self.title_label.pack(pady=10)

        self.combo_listbox = Listbox(self, selectmode="multiple", width=50, font=("Helvetica", 14), bg="#1a1a1a", fg="white", bd=2, relief="groove")
        self.combo_listbox.bind('<<ListboxSelect>>', self.update_total_price)
        for combo in self.combos:
            self.combo_listbox.insert("end", f"{combo.description} - ${combo.price:.2f}")
        self.combo_listbox.pack(pady=10)

        self.total_price_label = Label(self, text=f"Precio total estimado: ${self.total_price:.2f}", font=("Helvetica", 16, "bold"), bg="#000000", fg="white")
        self.total_price_label.pack(pady=10)

        self.summary_button = Button(self, text="Continuar", command=self.show_customization_window, font=("Helvetica", 14, "bold"), bg="#1a1a1a", fg="white", bd=2, relief="raised")
        self.summary_button.pack(pady=10)

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    # Método para cargar los combos desde la base de datos
    def load_combos(self):
        combos = self.combo_controller.get_combos()
        for combo in combos:
            print(combo)  
        return combos

    # Método para actualizar el precio total
    def update_total_price(self, event=None):
        selected_indices = self.combo_listbox.curselection()
        self.total_price = self.subtotal + sum(self.combos[i].price for i in selected_indices)
        self.total_price_label.config(text=f"Precio total estimado: ${self.total_price:.2f}")

    # Método para mostrar la ventana de personalización
    def show_customization_window(self):
        customization_window = Toplevel(self.master)
        customization_window.title("Personalizar Combo")
        customization_window.geometry("400x400")
        customization_window.configure(bg="#000000")

        Label(customization_window, text="Personalizar Combo", font=("Helvetica", 18, "bold"), bg="#000000", fg="white").pack(pady=10)

        # Opciones de palomitas
        Label(customization_window, text="Palomitas:", font=("Helvetica", 14), bg="#000000", fg="white").pack(pady=5)
        self.popcorn_size = IntVar()
        self.popcorn_size.trace("w", self.calculate_total_price)  # Actualizar precio en tiempo real
        Radiobutton(customization_window, text="Pequeñas (+$1)", variable=self.popcorn_size, value=1, bg="#000000", fg="white", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Normales (+$2)", variable=self.popcorn_size, value=2, bg="#000000", fg="white", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Grandes (+$3)", variable=self.popcorn_size, value=3, bg="#000000", fg="white", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")

        # Opciones de bebidas
        Label(customization_window, text="Bebidas:", font=("Helvetica", 14), bg="#000000", fg="white").pack(pady=5)
        self.drink_size = IntVar()
        self.drink_size.trace("w", self.calculate_total_price)  # Actualizar precio en tiempo real
        Radiobutton(customization_window, text="Pequeñas (+$1)", variable=self.drink_size, value=1, bg="#000000", fg="white", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Normales (+$2)", variable=self.drink_size, value=2, bg="#000000", fg="white", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Grandes (+$3)", variable=self.drink_size, value=3, bg="#000000", fg="white", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")

        self.custom_total_price_label = Label(customization_window, text=f"Precio total estimado: ${self.total_price:.2f}", font=("Helvetica", 16, "bold"), bg="#000000", fg="white")
        self.custom_total_price_label.pack(pady=10)

        Button(customization_window, text="Calcular Precio Total", command=self.open_promotions_view, font=("Helvetica", 14, "bold"), bg="#1a1a1a", fg="white", bd=2, relief="raised").pack(pady=20)

    # Método para calcular el precio total con personalización
    def calculate_total_price(self, *args):
        extra_price = self.popcorn_size.get() + self.drink_size.get()
        total_price = self.total_price + extra_price
        self.custom_total_price_label.config(text=f"Precio total estimado: ${total_price:.2f}")

    # Método para mostrar el resumen
    def show_summary(self):
        # Abrir la vista de promociones
        self.open_promotions_view()

    # Método para abrir la vista de promociones
    def open_promotions_view(self):
        self.master.withdraw()  # Ocultar la ventana de CombosSelectionView
        purchase_summary = {
            'movie': self.movie.title,
            'ticket_count': len(self.selected_seats),
            'seats': [f"{seat.row}{seat.number}" for seat in self.selected_seats],
            'combos': [self.combos[i].description for i in self.combo_listbox.curselection()],
            'promotions': [],
            'total': self.total_price
        }
        promotions_window = Toplevel(self.master)
        promotions_view = PromotionsView(promotions_window, purchase_summary, self.db_connection, self.email)
        promotions_view.pack()
        promotions_window.protocol("WM_DELETE_WINDOW", lambda: (self.master.deiconify(), promotions_window.destroy()))  # Mostrar la ventana principal cuando se cierre la nueva ventana

    def run(self):
        self.pack()
        
        self.master.mainloop()