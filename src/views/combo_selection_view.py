from tkinter import Frame, Label, Button, Listbox, StringVar, Entry, messagebox, Toplevel, Radiobutton, IntVar, Canvas, Scrollbar, Menu, Tk
from views.promotions_view import PromotionsView  # Asegúrate de importar la clase PromotionsView
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os
from controllers.combo_controller import ComboController
from views.user_detail_view import UserDetailView 

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
        self.total_price = subtotal
        self.combo_frames = {}  # Diccionario para almacenar los frames de los combos

        self.init_ui()

    # Método para inicializar la interfaz
    def init_ui(self):
        self.master.title("Selecciona tus combos")
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#ffffff")  # Fondo blanco

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=100)  # Fondo gris oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 30, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 200), pady=10)

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/image/image.jpg"):  # Reemplaza con la ruta de tu imagen
            navbar_image = Image.open("src/assets/image/image.jpg")
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

            # Crear el menú desplegable
            self.navbar_menu = Menu(self.navbar, tearoff=0, bg="#333333", fg="white", font=("Helvetica", 12), activebackground="#1a1a1a", activeforeground="white")
            self.navbar_menu.add_command(label="Ver perfil", command=self.open_user_detail_view)
            self.navbar_menu.add_command(label="Cerrar sesión", command=self.logout)
            
            # Asociar el menú desplegable a la imagen
            self.navbar_image_label.bind("<Button-1>", self.show_navbar_menu)

        # Contenedor central con borde negro
        self.container = Frame(self.master, bg="#ffffff", bd=2, relief="solid", highlightbackground="black", highlightthickness=2)
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

        self.title_label = Label(self.container, text=f"Selecciona tus combos para: {self.movie.title}", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="black")
        self.title_label.pack(pady=10)

        # Crear un canvas con scrollbar para la lista de combos
        self.canvas = Canvas(self.container, bg="#ffffff")
        self.scrollbar = Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#ffffff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Crear la lista de combos con imágenes
        self.create_combo_list()

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=100)
        self.footer.pack(side="bottom", fill="x")

        self.subtotal_label = Label(self.footer, text=f"Costo de boletos: ${self.subtotal:.2f}", font=("Helvetica", 16, "bold"), bg="#333333", fg="white")
        self.subtotal_label.pack(side="left", padx=20, pady=10)

        self.total_price_label = Label(self.footer, text=f"Precio total estimado: ${self.total_price:.2f}", font=("Helvetica", 16, "bold"), bg="#333333", fg="white")
        self.total_price_label.pack(side="left", padx=20, pady=10)

        self.summary_button = Button(self.footer, text="Continuar", command=self.show_customization_window, font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#333333", bd=2, relief="raised")
        self.summary_button.pack(side="right", padx=20, pady=10)

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(side="bottom", pady=10)

    # Método para cargar los combos desde la base de datos
    def load_combos(self):
        combos = self.combo_controller.get_combos()
        for combo in combos:
            print(combo)  
        return combos

    # Método para crear la lista de combos con imágenes
    def create_combo_list(self):
        for combo in self.combos:
            combo_frame = Frame(self.scrollable_frame, bg="#ffffff", bd=2, relief="solid", padx=10, pady=10, width=700)
            combo_frame.pack(fill="x", pady=5)
            self.combo_frames[combo] = combo_frame  # Almacenar el frame del combo
            index = 2
            # Cargar la imagen del combo
            image_path = f"src/assets/combos/combo{index}.jpg"  # Reemplaza con la ruta de tu imagen
            print(index)
            if os.path.exists(image_path):
                combo_image = Image.open(image_path)
                combo_image = combo_image.resize((100, 100), Image.LANCZOS)
                combo_photo = ImageTk.PhotoImage(combo_image)

                combo_image_label = Label(combo_frame, image=combo_photo, bg="#ffffff")
                combo_image_label.image = combo_photo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
                combo_image_label.pack(side="right", padx=10)
            index += 1
            
            combo_description = f"{combo.description} - ${combo.price:.2f}"
            combo_label = Label(combo_frame, text=combo_description, font=("Helvetica", 14), bg="#ffffff", fg="black", wraplength=500, justify="left")
            combo_label.pack(side="left", padx=10)

            combo_frame.bind("<Button-1>", lambda e, combo=combo: self.toggle_combo_selection(combo))

    # Método para alternar la selección de un combo
    def toggle_combo_selection(self, combo):
        if combo in self.selected_combos:
            self.selected_combos.remove(combo)
            self.combo_frames[combo].config(bg="#ffffff")  # Cambiar el fondo a blanco
        else:
            self.selected_combos.append(combo)
            self.combo_frames[combo].config(bg="#d3d3d3")  # Cambiar el fondo a gris claro
        self.update_total_price()

    # Método para actualizar el precio total
    def update_total_price(self, event=None):
        if not self.selected_combos:
            self.total_price = self.subtotal
        else:
            self.total_price = self.subtotal + sum(combo.price for combo in self.selected_combos)
        self.total_price_label.config(text=f"Precio total estimado: ${self.total_price:.2f}")

    # Método para mostrar la ventana de personalización
    def show_customization_window(self):
        if not self.selected_combos:
            return

        customization_window = Toplevel(self.master)
        customization_window.title("Adicionales")
        customization_window.geometry("600x600")
        customization_window.configure(bg="#ffffff")

        Label(customization_window, text="Adicionales", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="black").pack(pady=10)

        # Opciones de palomitas
        Label(customization_window, text="Palomitas:", font=("Helvetica", 14), bg="#ffffff", fg="black").pack(pady=5)
        self.popcorn_size = IntVar()
        self.popcorn_size.trace("w", self.calculate_total_price)  # Actualizar precio en tiempo real
        Radiobutton(customization_window, text="Pequeñas (+$1)", variable=self.popcorn_size, value=1, bg="#ffffff", fg="black", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Normales (+$2)", variable=self.popcorn_size, value=2, bg="#ffffff", fg="black", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Grandes (+$3)", variable=self.popcorn_size, value=3, bg="#ffffff", fg="black", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")

        # Opciones de bebidas
        Label(customization_window, text="Bebidas:", font=("Helvetica", 14), bg="#ffffff", fg="black").pack(pady=5)
        self.drink_size = IntVar()
        self.drink_size.trace("w", self.calculate_total_price)  # Actualizar precio en tiempo real
        Radiobutton(customization_window, text="Pequeñas (+$1)", variable=self.drink_size, value=1, bg="#ffffff", fg="black", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Normales (+$2)", variable=self.drink_size, value=2, bg="#ffffff", fg="black", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")
        Radiobutton(customization_window, text="Grandes (+$3)", variable=self.drink_size, value=3, bg="#ffffff", fg="black", selectcolor="#1a1a1a", font=("Helvetica", 12)).pack(anchor="w")

        self.custom_total_price_label = Label(customization_window, text=f"Precio total estimado: ${self.total_price:.2f}", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="black")
        self.custom_total_price_label.pack(pady=10)

        Button(customization_window, text="Calcular Precio Total", command=self.open_promotions_view, font=("Helvetica", 14, "bold"), bg="#333333", fg="white", bd=2, relief="raised").pack(pady=20)

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
            'combos': [combo.description for combo in self.selected_combos],
            'promotions': [],
            'total': self.total_price
        }
        promotions_window = Toplevel(self.master)
        promotions_view = PromotionsView(promotions_window, purchase_summary, self.db_connection, self.email, self.subtotal)
        promotions_view.pack()
        promotions_window.protocol("WM_DELETE_WINDOW", lambda: (self.master.deiconify(), promotions_window.destroy()))  # Mostrar la ventana principal cuando se cierre la nueva ventana

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