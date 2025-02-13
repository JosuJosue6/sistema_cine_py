class User:
    # Constructor de la clase
    def __init__(self, user_id, name , lastname, CI, email, password):
        self.user_id = user_id
        self.name = name
        self.lastname = lastname
        self.CI = CI
        self.email = email
        self.password = password
        #self.purchase_history = []

    # Agrega una compra a la lista de compras
    def add_purchase(self, purchase):
        self.purchase_history.append(purchase)

    # Retorna la lista de compras
    def get_purchase_history(self):
        return self.purchase_history

    # Retorna el usuario en formato string
    def __str__(self):
        return f"User(ID: {self.user_id}, Name: {self.name}, Lastaname: {self.lastname}, Email: {self.email}, CI: {self.CI}, Password: {self.password})"