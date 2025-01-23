from tkinter import Frame, Label, Button, StringVar, OptionMenu, messagebox

class TicketSelectionView(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.init_ui()

    #metodo para inicializar la interfaz
    def init_ui(self):
        self.ticket_type = StringVar()
        self.payment_method = StringVar()

        Label(self, text="Seleccione el tipo de boleto:").pack()

        ticket_options = ["Niño", "Adulto", "Adulto Mayor"]
        OptionMenu(self, self.ticket_type, *ticket_options).pack()

        Label(self, text="Seleccione el método de pago:").pack()

        payment_options = ["Tarjeta", "Contado"]
        OptionMenu(self, self.payment_method, *payment_options).pack()

        Button(self, text="Confirmar selección", command=self.confirm_selection).pack()

    #metodo para confirmar la seleccion del boleto
    def confirm_selection(self):
        ticket = self.ticket_type.get()
        payment = self.payment_method.get()

        if not ticket or not payment:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un tipo de boleto y un método de pago.")
            return

        #Aquí se puede agregar la lógica para calcular el precio y aplicar promociones
        messagebox.showinfo("Confirmación", f"Boleto: {ticket}\nMétodo de pago: {payment}")

    def run(self):
        self.pack()
        self.master.mainloop()