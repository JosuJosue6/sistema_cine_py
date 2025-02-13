class Combo:
    # Constructor
    def __init__(self, combo_id, description, price,image):
        self.combo_id = combo_id
        self.description = description
        self.price = price
        self.image = image

    # Retornar un string con la informacion del combo
    def __str__(self):
        return f"Combo ID: {self.combo_id}, Description: {self.description}, Price: {self.price}, Image: {self.image}"