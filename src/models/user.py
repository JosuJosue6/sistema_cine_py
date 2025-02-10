class User:
    #constructor de la clase
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.purchase_history = []

    #agrega una compra a la lista de compras
    def add_purchase(self, purchase):
        self.purchase_history.append(purchase)

    #retorna la lista de compras
    def get_purchase_history(self):
        return self.purchase_history

    #retorna el usuario en formato string
    def __str__(self):
        return f"User(ID: {self.user_id}, Name: {self.name}, Email: {self.email})"