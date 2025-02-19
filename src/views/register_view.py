from tkinter import Frame, Label, Entry, Button, messagebox, Toplevel
from controllers.user_controller import UserController
from PIL import Image, ImageTk, ImageDraw
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mailjet_rest import Client
import base64
import re
import requests

class RegisterUserView(Frame):
    def __init__(self, master, db_connection):
        super().__init__(master)
        self.master = master
        self.db_connection = db_connection
        self.user_controller = UserController(db_connection)
        self.bg_photo = None
        self.bg_label = None

        #self.bg_image = "src/assets/cine1.jpeg" 
        #self.bg_image = "src/assets/cine2.jpeg" 
        #self.bg_image = "src/assets/cine3.jpeg" 
        #self.bg_image = "src/assets/cine4.jpeg" 
        self.bg_image = "src/assets/Test.jpg"

        self.init_ui()

    def init_ui(self):
        self.master.title("Registrar Usuario")
        self.master.state('zoomed')
        self.master.configure(bg="#000000")

        # Cargar la imagen de fondo
        self.load_background_image()

        # Redimensionar la imagen de fondo cuando la ventana cambie de tamaño
        self.master.bind("<Configure>", self.resize_background)

         # Navbar
        self.navbar = Frame(self.master, bg="#333333", height=70)
        self.navbar.pack(side="top", fill="x")

        self.navbar_label = Label(self.navbar, text="Sistema de CINE", font=("Helvetica", 24, "bold"), bg="#333333", fg="white", padx=10)
        self.navbar_label.pack(side="left", padx=(10, 400), pady=10)

        if os.path.exists("src/assets/image/image.jpg"):
            navbar_image = Image.open("src/assets/image/image.jpg")
            navbar_image = navbar_image.resize((50, 50), Image.LANCZOS)

            mask = Image.new("L", navbar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + navbar_image.size, fill=255)
            navbar_image.putalpha(mask)

            navbar_photo = ImageTk.PhotoImage(navbar_image)

            self.navbar_image_label = Label(self.navbar, image=navbar_photo, bg="#333333")
            self.navbar_image_label.image = navbar_photo
            self.navbar_image_label.pack(side="right", padx=10, pady=10)

         # Main container with border
        self.container = Frame(self.master, bg="#f0f0f0", bd=2, relief="solid", highlightbackground="black", highlightthickness=2)
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=600)

        self.title_label = Label(self.container, text="Registrar Usuario", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=5)

        self.name_label = Label(self.container, text="Nombre:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self.container, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.lastname_label = Label(self.container, text="Apellido:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.lastname_label.pack(pady=5)
        self.lastname_entry = Entry(self.container, font=("Arial", 12))
        self.lastname_entry.pack(pady=5)

        self.ci_label = Label(self.container, text="CI:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.ci_label.pack(pady=5)
        self.ci_entry = Entry(self.container, font=("Arial", 12))
        self.ci_entry.pack(pady=5)

        self.email_label = Label(self.container, text="Correo Electrónico:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self.container, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        self.password_label = Label(self.container, text="Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.password_label.pack(pady=5)
        self.password_entry = Entry(self.container, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        self.confirm_password_label = Label(self.container, text="Confirmar Contraseña:", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.confirm_password_label.pack(pady=5)
        self.confirm_password_entry = Entry(self.container, font=("Arial", 12), show="*")
        self.confirm_password_entry.pack(pady=5)

        button_width = 20  

        self.register_button = Button(self.container, text="Registrar", font=("Arial", 12, "bold"), bg="#333", fg="white", command=self.register_user, width=button_width)
        self.register_button.pack(pady=10)

       # Footer
        self.footer = Frame(self.master, bg="#333333", height=50)
        self.footer.pack(side="bottom", fill="x")

        self.footer_label = Label(self.footer, text="© 2025 Sistema de Cine. Todos los derechos reservados.", font=("Helvetica", 10), bg="#333333", fg="white")
        self.footer_label.pack(pady=10)
        
    def load_background_image(self):
        if os.path.exists(self.bg_image):  # Reemplaza con la ruta de tu imagen de fondo
            bg_image = Image.open(self.bg_image)
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = Label(self.master, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            #self.bg_label.lower()

    def resize_background(self, event):
        if self.bg_photo:
            screen_width = self.master.winfo_width()
            screen_height = self.master.winfo_height()
            bg_image = Image.open(self.bg_image)
            bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label.config(image=self.bg_photo)

    def register_user(self):
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        ci = self.ci_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not name or not lastname or not ci or not email or not password or not confirm_password:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        if password != confirm_password:
            messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
            return
        
        # Validar el formato del correo electrónico
        if not self.is_valid_email(email):
            messagebox.showwarning("Advertencia", "El correo electrónico no tiene un formato válido.")
            return
        
        # Verificar si el correo electrónico existe
        if not self.verify_email_exists(email):
            messagebox.showwarning("Advertencia", "El correo electrónico no existe.")
            return

        user_data = {
            'name': name,
            'lastname': lastname,
            'CI': ci,
            'email': email,
            'password': password
        }

        try:
            if self.send_verification_email(email):
                self.user_controller.create_user(user_data)
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente. Se ha enviado un correo de verificación, si no lo recibio, verifique su email.")
                self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario. Error: {e}")

    def is_valid_email(self, email):
        # Expresión regular para validar el formato del correo electrónico
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email) is not None

    def verify_email_exists(self, email):
        api_key = "d76a2c3e8c2e1b2825a200a70bdeb361e7588019"  
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data['data']['status'] == 'valid':
            print("Correo electrónico válido")
            return True
        else:
            return False

    def send_verification_email(self, email):
        api_key = "173d140b1aa3661cc8b4c5128fce73e7"
        api_secret = "90ab1e9875b79c52e61e01aaeb403f11"
        from_email = "testpruebasvsc@gmail.com"
        subject = "Verificación de correo electrónico"
        body = "Gracias por registrarte. Por favor, su correo fue registrado con exito, si no identifica este mensaje contactenos."

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
                            "Email": email,
                            "Name": "Nuevo Usuario"
                        }
                    ],
                    "Subject": subject,
                    "TextPart": body
                }
            ]
        }

        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print("Correo de verificación enviado exitosamente")
            return True
        else:
            messagebox.showerror("Error de Envío", "No se pudo enviar el correo electrónico. Verifica tu correo.")
            print(f"Error: {result.status_code}")
            print(result.json())
            return False

    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.lastname_entry.delete(0, 'end')
        self.ci_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')

    def run(self):
        self.pack()
        self.master.mainloop()