from tkinter import Frame, Label, Listbox, Button, StringVar, Entry, END, messagebox

class ComboSelectionView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.combos = self.load_combos()

    # Método para crear los widgets de la interfaz
    def create_widgets(self):
        
        self.title_label = Label(self, text="Seleccione sus Combos", font=("Arial", 16))
        self.title_label.pack(pady=10)

        #listbox para mostrar los combos disponibles
        self.combo_listbox = Listbox(self, selectmode='multiple')
        self.combo_listbox.pack(pady=10)

        self.customization_label = Label(self, text="Personalización (opcional):")
        self.customization_label.pack(pady=5)

        self.extra_popcorn_var = StringVar()
        self.extra_popcorn_entry = Entry(self, textvariable=self.extra_popcorn_var)
        self.extra_popcorn_entry.pack(pady=5)
        self.extra_popcorn_entry.insert(0, "Extra de palomitas (cantidad)")

        self.submit_button = Button(self, text="Agregar Combos", command=self.add_combos)
        self.submit_button.pack(pady=10)

        self.summary_button = Button(self, text="Ver Resumen", command=self.show_summary)
        self.summary_button.pack(pady=10)
    
    #cargar los combos desde la base de datos
    def load_combos(self):
        # Simulación de carga de combos desde la base de datos
        return [
            {"id": 1, "description": "Combo 1: Palomitas grandes + 2 refrescos", "price": 10.00},
            {"id": 2, "description": "Combo 2: Nachos + 1 refresco", "price": 8.00},
            {"id": 3, "description": "Combo 3: Palomitas medianas + 1 refresco", "price": 7.00},
        ]

    # metodo para agregar los combos seleccionados
    def add_combos(self):
        selected_indices = self.combo_listbox.curselection()
        selected_combos = [self.combos[i] for i in selected_indices]
        extra_popcorn = self.extra_popcorn_var.get()

        if selected_combos:
            messagebox.showinfo("Combos Agregados", f"Combos seleccionados: {selected_combos}\nExtra de palomitas: {extra_popcorn}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione al menos un combo.")

    #metodo para mostrar el resumen de la compra
    def show_summary(self):
        # Aquí se mostraría el resumen de la compra
        messagebox.showinfo("Resumen de Compra", "Aquí se mostraría el resumen de la compra.")

    #metodo para iniciar la interfaz
    def run(self):
        self.mainloop()