class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def get_total_price(self):
        return self.price * self.quantity
    def calculate_shipping(self, weight_kg, region="default"):
        """Рассчитывает стоимость доставки."""
        rates = {"default": 10, "express": 30, "international": 200}
        return rates.get(region, rates["default"]) / weight_kg