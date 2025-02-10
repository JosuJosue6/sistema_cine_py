from tkinter import Frame, Label, Button, messagebox
import qrcode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from controllers.user_controller import UserController  
from PIL import Image, ImageTk, ImageDraw  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SummaryView(Frame):
    def __init__(self, master, purchase_summary, db_connection, user_email):
        super().__init__(master)
        self.master = master
        self.purchase_summary = purchase_summary
        self.db_connection = db_connection
        self.user_email = user_email
        self.user_controller = UserController(db_connection)
        self.init_ui()

    def init_ui(self):
        self.master.title("Resumen de Compra")
        self.master.configure(bg="#ffffff")  # Fondo blanco
        self.master.state('zoomed')

        # Barra de navegación
        self.navbar = Frame(self.master, bg="#333333", height=70)  # Fondo gris oscuro
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

        # Cargar la imagen para la navbar
        if os.path.exists("src/assets/movies/movie1.jpg"):  # Reemplaza con la ruta de tu imagen
            navbar_image = Image.open("src/assets/movies/movie1.jpg")
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

        self.title_label = Label(self.master, text="Resumen de Compra", font=("Arial", 24, "bold"), bg="#ffffff", fg="black")
        self.title_label.pack(pady=10)

        self.movie_label = Label(self.master, text=f"Película: {self.purchase_summary['movie']}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.movie_label.pack(pady=5)

        self.seats_label = Label(self.master, text=f"Asientos: {', '.join(self.purchase_summary['seats'])}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.seats_label.pack(pady=5)

        self.combos_label = Label(self.master, text=f"Combos: {', '.join(self.purchase_summary['combos'])}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.combos_label.pack(pady=5)

        self.promotions_label = Label(self.master, text=f"Promociones aplicadas: {', '.join(self.purchase_summary['promotions'])}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.promotions_label.pack(pady=5)

        self.total_label = Label(self.master, text=f"Total a pagar: ${self.purchase_summary['total']:.2f}", font=("Arial", 14), bg="#ffffff", fg="black")
        self.total_label.pack(pady=10)

        self.confirm_button = Button(self.master, text="Confirmar Compra", command=self.confirm_purchase, font=("Arial", 14, "bold"), bg="#333333", fg="white", activebackground="#555555", activeforeground="#ffffff", relief="raised", bd=2)
        self.confirm_button.pack(pady=20)

        # Pie de página
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)

    def confirm_purchase(self):
        # Generar el código QR con la información del resumen
        qr_data = f"Película: {self.purchase_summary['movie']}\nAsientos: {', '.join(self.purchase_summary['seats'])}\nCombos: {', '.join(self.purchase_summary['combos'])}\nTotal: ${self.purchase_summary['total']:.2f}"
        qr = qrcode.make(qr_data)
        qr_path = "purchase_qr.png"
        qr.save(qr_path)

        # Generar el PDF con la información del resumen y el código QR
        pdf_path = "purchase_summary.pdf"
        self.generate_pdf(pdf_path, qr_path)

        # Enviar el correo electrónico con el PDF adjunto
        self.send_email(self.user_email, pdf_path)

        messagebox.showinfo("Confirmación", "Compra confirmada y correo enviado con el PDF de la factura.")

    def generate_pdf(self, pdf_path, qr_path):
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
        c.drawImage(qr_path, 100, height - 400, width=200, height=200)

        # Información adicional de la factura
        c.setFont("Times-Bold", 16)
        c.drawString(100, height - 450, "Información de Contacto")
        c.setFont("Times-Roman", 14)
        c.drawString(100, height - 470, f"Nombre del Cliente: {self.user_email.split('@')[0].replace('.', ' ').title()}")
        c.drawString(100, height - 490, f"Correo Electrónico: {self.user_email}")
        c.drawString(100, height - 510, "Fecha de Compra: 08/02/2025")

        c.save()

    def send_email(self, to_email, pdf_path):
        from_email = "testpruebasvsc@gmail.com"
        from_password = "tu_contraseña"
        subject = "Confirmación de Compra - Sistema de Cine"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        body = "Gracias por tu compra. Adjuntamos el PDF con los detalles de tu compra y el código QR."
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(pdf_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_path)}")
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

    def run(self):
        self.pack()
        self.master.mainloop()