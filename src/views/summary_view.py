from tkinter import Button, Label


class SummaryView:
    def __init__(self, master, purchase_summary):
        self.master = master
        self.purchase_summary = purchase_summary
        self.create_widgets()

    # Crear los widgets de la interfaz
    def create_widgets(self):
        self.title_label = Label(self.master, text="Resumen de Compra", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.movie_label = Label(self.master, text=f"Película: {self.purchase_summary['movie']}")
        self.movie_label.pack(pady=5)

        self.tickets_label = Label(self.master, text=f"Número de boletos: {self.purchase_summary['ticket_count']}")
        self.tickets_label.pack(pady=5)

        self.combo_label = Label(self.master, text=f"Combos agregados: {', '.join(self.purchase_summary['combos'])}")
        self.combo_label.pack(pady=5)

        self.promotions_label = Label(self.master, text=f"Promociones aplicadas: {', '.join(self.purchase_summary['promotions'])}")
        self.promotions_label.pack(pady=5)

        self.total_label = Label(self.master, text=f"Total a pagar: ${self.purchase_summary['total']:.2f}")
        self.total_label.pack(pady=10)

        self.confirm_button = Button(self.master, text="Confirmar Compra", command=self.confirm_purchase)
        self.confirm_button.pack(pady=20)

    def confirm_purchase(self):
        # Logic to handle purchase confirmation (e.g., generate QR code, send email)
        pass