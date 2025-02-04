from tkinter import Frame, Label, Button, messagebox
import qrcode
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from controllers.user_controller import UserController  # Asegúrate de tener un controlador de usuario para obtener el correo electrónico del usuario

class SummaryView(Frame):
    def __init__(self, master, purchase_summary, db_connection):
        super().__init__(master)
        self.master = master
        self.purchase_summary = purchase_summary
        self.db_connection = db_connection
        self.user_controller = UserController(db_connection)
        self.init_ui()

    def init_ui(self):
        self.master.title("Resumen de Compra")
        # Maximizar la ventana
        self.master.state('zoomed')
        self.master.configure(bg="#ffffff")  # Fondo blanco

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

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Arial", 10), bg="#333333", fg="black")
        self.footer_label.pack(pady=10)

    def confirm_purchase(self):
        # Generar el código QR con la información del resumen
        qr_data = f"Película: {self.purchase_summary['movie']}\nAsientos: {', '.join(self.purchase_summary['seats'])}\nCombos: {', '.join(self.purchase_summary['combos'])}\nTotal: ${self.purchase_summary['total']:.2f}"
        qr = qrcode.make(qr_data)
        qr_path = "purchase_qr.png"
        qr.save(qr_path)

        # Obtener el correo electrónico del usuario desde la base de datos
        user_email = self.user_controller.get_user_email(2)
        if not user_email:
            messagebox.showerror("Error", "No se pudo obtener el correo electrónico del usuario.")
            return

        # Enviar el correo electrónico con el código QR adjunto
        self.send_email(user_email, qr_path)

        messagebox.showinfo("Confirmación", "Compra confirmada y correo enviado con el código QR.")

    def send_email(self, to_email, qr_path):
        from_email = "tu_correo@gmail.com"
        from_password = "tu_contraseña"
        subject = "Confirmación de Compra - Sistema de Cine"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        body = "Gracias por tu compra. Adjuntamos el código QR con los detalles de tu compra."
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(qr_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(qr_path)}")
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