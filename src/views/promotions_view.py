from tkinter import Frame, Label, Listbox, StringVar, Scrollbar, messagebox, Button
from models.promotion import Promotion  
from controllers.promotion_controller import PromotionController  

class PromotionsView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.load_promotions()

    def create_widgets(self):
        self.title_label = Label(self, text="Promociones Vigentes", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.promotion_list = Listbox(self, width=50, height=10)
        self.promotion_list.pack(pady=10)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")
        self.promotion_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.promotion_list.yview)

        self.select_button = Button(self, text="Seleccionar Promoción", command=self.select_promotion)
        self.select_button.pack(pady=10)

    def load_promotions(self):
        self.promotion_list.delete(0, 'end')
        promotions = PromotionController.get_active_promotions()  # Fetch promotions from the controller
        for promotion in promotions:
            self.promotion_list.insert('end', f"{promotion.description} - {promotion.discount}% off")

    def select_promotion(self):
        try:
            selected_index = self.promotion_list.curselection()[0]
            selected_promotion = self.promotion_list.get(selected_index)
            messagebox.showinfo("Promoción Seleccionada", f"Has seleccionado: {selected_promotion}")
        except IndexError:
            messagebox.showwarning("Selección Inválida", "Por favor, selecciona una promoción.")