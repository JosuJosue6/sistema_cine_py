class Promotion:
    def __init__(self, promotion_id, description, discount):
        self.promotion_id = promotion_id
        self.description = description
        self.discount = discount

    def __str__(self):
        return f"{self.description} - {self.discount}% off"