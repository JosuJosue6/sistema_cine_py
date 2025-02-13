from tkinter import Frame, Label, Listbox, Button, messagebox, Toplevel, Menu, Tk
from controllers.promotion_controller import PromotionController
from views.summary_view import SummaryView  # Asegúrate de importar la clase SummaryView
from decimal import Decimal
from PIL import Image, ImageTk, ImageDraw  # Necesitarás instalar Pillow para manejar imágenes
import os
from views.user_detail_view import UserDetailView 

class PromotionsView(Frame):
    def __init__(self, master=None, purchase_summary=None, database=None, user_email=None, ticket_price=None):
        super().__init__(master)
        self.master = master
        self.db = database
        self.ticket_price = ticket_price
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
        self.master.title("Promociones")
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="white")  # Fondo blanco

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=100)  # Fondo gris oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

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
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        self.title_label = Label(self.container, text="Promociones Vigentes", font=("Helvetica", 18, "bold"), bg="white", fg="black")
        self.title_label.pack(pady=10)

        self.promotion_list = Listbox(self.container, width=50, font=("Helvetica", 14), bg="#ecf0f1", fg="#2c3e50", bd=2, relief="groove")
        self.promotion_list.pack(pady=10)

        self.select_button = Button(self.container, text="Seleccionar Promoción", command=self.select_promotion, font=("Helvetica", 14, "bold"), bg="#333333", fg="white", bd=2, relief="raised")
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
            self.purchase_summary['total'] = Decimal(self.purchase_summary['total'])  # Convertir a Decimal si no lo es

            # Si se selecciona la primera o tercera opción
            if selected_index == 0 or selected_index == 2:
                discounted_amount = (self.purchase_summary['total'] - self.ticket_price) * (discount / Decimal('100'))
                self.purchase_summary['total'] -= discounted_amount
            # Si se selecciona la segunda opción
            elif selected_index == 1:
               discounted_amount = self.ticket_price * (discount / Decimal('100'))
               self.purchase_summary['total'] -= discounted_amount
            else:
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
        user_detail_view = UserDetailView(user_detail_window, self.db, self.email)
        user_detail_view.pack(fill="both", expand=True)
        user_detail_window.mainloop()

    def logout(self):
        from views.login_view import LoginView
        self.master.destroy()
        login_window = Tk()
        login_view = LoginView(login_window, self.db)
        login_view.pack(fill="both", expand=True)
        login_window.mainloop() 