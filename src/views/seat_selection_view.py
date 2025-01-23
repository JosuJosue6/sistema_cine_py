from tkinter import Frame, Label, Button, messagebox
from models.seat import Seat
from controllers.seat_controller import SeatController

class SeatSelectionView(Frame):
    def __init__(self, master, movie):
        super().__init__(master)
        self.master = master
        self.movie = movie
        self.seat_controller = SeatController()
        self.selected_seats = []

        self.init_ui()

    #metodo para inicializar la interfaz
    def init_ui(self):
        self.title_label = Label(self, text=f"Selecciona tus asientos para: {self.movie.title}")
        self.title_label.pack()

        self.seat_buttons = self.create_seat_buttons()
        for button in self.seat_buttons:
            button.pack(side="left")

        self.confirm_button = Button(self, text="Confirmar selección", command=self.confirm_selection)
        self.confirm_button.pack()

    #metodo para crear los botones de los asientos
    def create_seat_buttons(self):
        seats = self.seat_controller.get_available_seats(self.movie.id)
        buttons = []
        for seat in seats:
            button = Button(self, text=f"{seat.row}{seat.number}", command=lambda s=seat: self.toggle_seat(s))
            button.config(bg="green" if seat.availability else "red")
            buttons.append(button)
        return buttons
    
    #metodo para alternar la seleccion de un asiento
    def toggle_seat(self, seat):
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            self.update_button_color(seat, "green")
        else:
            self.selected_seats.append(seat)
            self.update_button_color(seat, "yellow")

    #metodo para actualizar el color de un boton de asiento
    def update_button_color(self, seat, color):
        for button in self.seat_buttons:
            if button.cget("text") == f"{seat.row}{seat.number}":
                button.config(bg=color)

    #metodo para confirmar la seleccion de asientos
    def confirm_selection(self):
        if not self.selected_seats:
            messagebox.showwarning("Advertencia", "Por favor selecciona al menos un asiento.")
            return

        # Validar la selección de asientos
        messagebox.showinfo("Confirmación", f"Asientos seleccionados: {', '.join([f'{s.row}{s.number}' for s in self.selected_seats])}")


    def run(self):
        self.pack()
        self.master.mainloop()