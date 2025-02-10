from tkinter import Frame, Label, Listbox, Button, Scrollbar, messagebox, Toplevel
from controllers.promotion_controller import PromotionController
from views.summary_view import SummaryView  # Asegúrate de importar la clase SummaryView
from decimal import Decimal
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os

class PromotionsView(Frame):
    def __init__(self, master=None, purchase_summary=None, database=None, user_email=None):
        super().__init__(master)
        self.master = master
        self.db = database
        self.user_email = user_email
        self.purchase_summary = purchase_summary if purchase_summary is not None else {
            'movie': '',
            'ticket_count': 0,
            'combos': [],
            'seats': [],
            'promotions': [],
            'total': Decimal('10.0')
        }
        self.create_widgets()
        self.load_promotions()

    def create_widgets(self):
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="white")  # Fondo oscuro

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=100)  # Fondo rojo
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

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

        self.title_label = Label(self, text="Promociones Vigentes", font=("Helvetica", 18, "bold"), bg="white", fg="black")
        self.title_label.pack(pady=10)

        self.promotion_list = Listbox(self, width=50, font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50", bd=2, relief="groove")
        self.promotion_list.pack(pady=10)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")
        self.promotion_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.promotion_list.yview)

        self.select_button = Button(self, text="Seleccionar Promoción", command=self.select_promotion, font=("Helvetica", 14, "bold"), bg="#333333", fg="white", bd=2, relief="raised")
        self.select_button.pack(pady=10)

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    def load_promotions(self):
        self.promotion_list.delete(0, 'end')
        promotions = PromotionController.get_active_promotions() 
        for promotion in promotions:
            self.promotion_list.insert('end', f"{promotion.description} - {promotion.discount}% off")

    def select_promotion(self):
        try:
            selected_index = self.promotion_list.curselection()[0]
            selected_promotion = self.promotion_list.get(selected_index)
            messagebox.showinfo("Promoción Seleccionada", f"Has seleccionado: {selected_promotion}")
            # Agregar la promoción seleccionada al resumen de la compra
            self.purchase_summary['promotions'].append(selected_promotion)
            # Aplicar el descuento al total
            discount = Decimal(selected_promotion.split('-')[-1].strip('% off'))
            self.purchase_summary['total'] -= self.purchase_summary['total'] * (discount / Decimal('100'))
            # Abrir la vista de resumen
            self.open_summary_view()
        except IndexError:
            messagebox.showwarning("Selección Inválida", "Por favor, selecciona una promoción.")

    # Método para abrir la vista de resumen
    def open_summary_view(self):
        self.master.withdraw()  # Ocultar la ventana de PromotionsView
        summary_window = Toplevel(self.master)
        summary_view = SummaryView(summary_window, self.purchase_summary, self.db, self.user_email)
        summary_view.pack()
        summary_window.protocol("WM_DELETE_WINDOW", lambda: (self.master.deiconify(), summary_window.destroy()))  # Mostrar la ventana principal cuando se cierre la nueva ventana