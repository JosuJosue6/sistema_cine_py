class ComboController:
    def __init__(self, combo_model):
        self.combo_model = combo_model

    #obtener todos los combos
    def get_combos(self):
        return self.combo_model.get_all_combos()

    #obtener un combo por su id y personalizarlo con extras
    def customize_combo(self, combo_id, extras):
        #obtener el combo por su id
        combo = self.combo_model.get_combo_by_id(combo_id)
        if combo:
            #personalizar el combo con los extras
            combo['extras'] = extras
            return combo
        return None

    #calcular el precio total de un combo
    def calculate_combo_price(self, combo):
        base_price = combo['price']
        extras_price = sum(extra['price'] for extra in combo.get('extras', []))
        return base_price + extras_price

    #aplicar promociones al precio de un combo
    def apply_promotions(self, combo_price, promotions):
        for promotion in promotions:
            if promotion['type'] == 'discount':
                combo_price -= combo_price * (promotion['value'] / 100)
        return combo_price