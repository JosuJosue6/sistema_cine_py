import base64
from tkinter import Frame, Label, Button, messagebox, Toplevel, Menu, Tk
import qrcode
import os
from controllers.user_controller import UserController  
from PIL import Image, ImageTk, ImageDraw  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mailjet_rest import Client
from views.user_detail_view import UserDetailView  
from datetime import datetime

class SummaryView(Frame):
    def __init__(self, master, purchase_summary, db_connection, user_email):
        super().__init__(master)
        self.master = master
        self.purchase_summary = purchase_summary
        self.db_connection = db_connection
        self.user_email = user_email
        self.user_controller = UserController(db_connection)

        #self.bg_image = "src/assets/cine1.jpeg" 
        #self.bg_image = "src/assets/cine2.jpeg" 
        #self.bg_image = "src/assets/cine3.jpeg" 
        #self.bg_image = "src/assets/cine4.jpeg" 
        self.bg_image = "src/assets/Test.jpg"
        self.init_ui()

    def init_ui(self):
        self.master.title("Resumen de Compra")
        self.master.configure(bg="#ffffff")  # Fondo blanco
        self.master.state('zoomed')

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=70)  # Fondo gris oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/image/image.jpg"):  # Reemplaza con la ruta de tu imagen
            navbar_image = Image.open("src/assets/image/image.jpg")
            navbar_image = navbar_image.resize((50, 50), Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS

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
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=600, height=600)

        self.container_info = Frame (self.container, bg="#ffffff", bd=2, relief="solid", highlightbackground="black", highlightthickness=2)
        self.container_info.place(relx=0.5, rely=0.5, anchor="center", width=600, height=600)
        self.title_label = Label(self.container_info, text="Resumen de Compra", font=("Arial", 24, "bold"), bg="#ffffff", fg="black")
        self.title_label.pack(pady=10)

        self.movie_label = Label(self.container_info, text=f"Película: {self.purchase_summary['movie']}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.movie_label.pack(pady=5)

        self.seats_label = Label(self.container_info, text=f"Asientos: {', '.join(self.purchase_summary['seats'])}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.seats_label.pack(pady=5)

        self.combos_label = Label(self.container_info, text=f"Combos: {', '.join(self.purchase_summary['combos'])}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.combos_label.pack(pady=5)

        self.promotions_label = Label(self.container_info, text=f"Promociones aplicadas: {', '.join(self.purchase_summary['promotions'])}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.promotions_label.pack(pady=5)

        self.total_label = Label(self.container_info, text=f"Total a pagar: ${self.purchase_summary['total']:.2f}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.total_label.pack(pady=20)

        self.confirm_button = Button(self.container_info, text="Confirmar Compra", command=self.confirm_purchase, font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        self.confirm_button.pack(pady=20)

        #self.new_purchase_button = Button(self.container, text="Realizar Nueva Compra", command=self.new_purchase, font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        #self.new_purchase_button.pack(pady=10)
#        self.new_purchase_button.pack_forget()  # Ocultar inicialmente

        self.exit_button = Button(self.container_info, text="Salir", command=self.master.quit, font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        self.exit_button.pack(pady=10)
        self.exit_button.pack_forget()  # Ocultar inicialmente

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    def confirm_purchase(self):
        # Generar el PDF con la información del resumen y el código QR
        pdf_path = "purchase_summary.pdf"
        self.generate_pdf(pdf_path)

        # Generar el código QR con los detalles de la compra en texto
        qr_data = f"Película: {self.purchase_summary['movie']}\nAsientos: {', '.join(self.purchase_summary['seats'])}\nCombos: {', '.join(self.purchase_summary['combos'])}\nPromociones aplicadas: {', '.join(self.purchase_summary['promotions'])}\nTotal a pagar: ${self.purchase_summary['total']:.2f}"
        qr = qrcode.make(qr_data)
        qr_path = "purchase_qr.png"
        qr.save(qr_path)

        # Enviar el correo electrónico con el PDF adjunto
        self.send_email(self.user_email, pdf_path, qr_path)

        messagebox.showinfo("Confirmación", "Compra confirmada y correo enviado con el PDF de la factura.")

        # Desactivar el botón de confirmar compra
        self.confirm_button.config(state="disabled")

        # Mostrar los botones de nueva compra y salir
       # self.new_purchase_button.pack(pady=10)
        self.exit_button.pack(pady=10)

    def generate_pdf(self, pdf_path):
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Título
        c.setFont("Times-Bold", 24)
        c.drawString(100, height - 100, "Factura de Compra")

        # Detalles de la compra
        c.setFont("Times-Roman", 14)
        c.drawString(100, height - 150, f"Película: {self.purchase_summary['movie']}")
        c.drawString(100, height - 170, f"Asientos: {', '.join(self.purchase_summary['seats'])}")
        c.drawString(100, height - 190, f"Combos: {', '.join(self.purchase_summary['combos'])}")
        c.drawString(100, height - 210, f"Promociones aplicadas: {', '.join(self.purchase_summary['promotions'])}")
        c.drawString(100, height - 230, f"Total a pagar: ${self.purchase_summary['total']:.2f}")

        # Código QR
        qr_path = "purchase_qr.png"
        c.drawImage(qr_path, 200, height - 430, width=150, height=150)

        # Información adicional de la factura
        c.setFont("Times-Bold", 16)
        c.drawString(100, height - 450, "Información de Contacto")
        c.setFont("Times-Roman", 14)
        c.drawString(100, height - 470, f"Nombre del Cliente: {self.user_email.split('@')[0].replace('.', ' ').title()}")
        c.drawString(100, height - 490, f"Correo Electrónico: {self.user_email}")
        fecha = datetime.now().strftime("%d/%m/%Y")
        c.drawString(100, height - 510, f"Fecha de Compra: {fecha}")

        c.save()

    def send_email(self, to_email, pdf_path, qr_path):
        api_key = "173d140b1aa3661cc8b4c5128fce73e7"
        api_secret = "90ab1e9875b79c52e61e01aaeb403f11"
        from_email = "testpruebasvsc@gmail.com"
        subject = "Confirmación de Compra - Sistema de Cine"
        body = "Gracias por tu compra. Adjuntamos el PDF con los detalles de tu compra y el código QR."

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": from_email,
                        "Name": "Sistema de Cine"
                    },
                    "To": [
                        {
                            "Email": to_email,
                            "Name": "Cliente"
                        }
                    ],
                    "Subject": subject,
                    "TextPart": body,
                    "Attachments": [
                        {
                            "ContentType": "application/pdf",
                            "Filename": os.path.basename(pdf_path),
                            "Base64Content": base64.b64encode(open(pdf_path, "rb").read()).decode('utf-8')
                        },
                        {
                            "ContentType": "image/png",
                            "Filename": os.path.basename(qr_path),
                            "Base64Content": base64.b64encode(open(qr_path, "rb").read()).decode('utf-8')
                        }
                    ]
                }
            ]
        }

        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print("Correo enviado exitosamente")
        else:
            messagebox.showerror("Error de Envío", "No se pudo enviar el correo electrónico. Verifica tu configuración.")
            print(f"Error: {result.status_code}")
            print(result.json())

    def run(self):
        self.pack()
        self.master.mainloop()

    def load_background_image(self):
        if os.path.exists(self.bg_image):  # Reemplaza con la ruta de tu imagen de fondo
            bg_image = Image.open(self.bg_image)
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
            bg_image = Image.open(self.bg_image)
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label.config(image=self.bg_photo)

    def logout(self):
        from views.login_view import LoginView
        self.master.destroy()
        login_window = Tk()
        login_view = LoginView(login_window, self.db_connection)
        login_view.pack(fill="both", expand=True)
        login_window.mainloop() 
    
    def show_navbar_menu(self, event):
        self.navbar_menu.post(event.x_root, event.y_root)

    def open_user_detail_view(self):
        user_detail_window = Toplevel(self.master)
        user_detail_view = UserDetailView(user_detail_window, self.db_connection, self.email)
        user_detail_view.pack(fill="both", expand=True)
        user_detail_window.mainloop()
