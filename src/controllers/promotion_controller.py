from models.promotion import Promotion

class PromotionController:
    @staticmethod
    def get_active_promotions():
        return [
            Promotion(1, "Descuento en palomitas", 10),
            Promotion(2, "2x1 en entradas", 50),
            Promotion(3, "Descuento en bebidas", 20),
        ]