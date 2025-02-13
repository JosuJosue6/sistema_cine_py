from models.combo import Combo

class ComboController:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    #buscar todos los combos
    def get_combos(self):
        query = "SELECT * FROM Combos"
        result = self.db_connection.execute_query(query)
        if result:
            combos = [Combo(row[0], row[1], row[2],row[3]) for row in result]
            return combos
        return []

    #buscar combos por id
    def get_combo_by_id(self, combo_id):
        query = f"SELECT * FROM Combos WHERE ID={combo_id}"
        result = self.db_connection.execute_query(query)
        if result:
            return result[0]
        return None

    # personalizar un combo con extras
    def customize_combo(self, combo_id, extras):
        combo = self.get_combo_by_id(combo_id)
        if combo:
            combo['extras'] = extras
            return combo
        return None
    
    # calcular el precio de un combo
    def calculate_combo_price(self, combo, extra):
        base_price = combo['price']
        return base_price + extra


    #aplicar promociones al precio de un combo
    def apply_promotions(self, combo_price, promotions):
        for promotion in promotions:
            if promotion['type'] == 'discount':
                combo_price -= combo_price * (promotion['value'] / 100)
        return combo_price