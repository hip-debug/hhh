from .exceptions import ValidationError, NegativePriceError, InsufficientStockError


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self._price = None
        self.quantity = quantity
        self.set_price(price)

    def check_stock(self):
        return self.quantity

    def update_stock(self, amount):

        if amount <= 0:
            raise ValidationError(f"Количество для пополнения должно быть положительным: {amount}")

        self.quantity += amount
        return self.quantity

    @property
    def price(self):
        return self._price

    def set_price(self, price):
        if price < 0:
            raise NegativePriceError(f"Цена не может быть отрицательной: {price}")
        self._price = price

    def get_total_price(self):
        return self.price * self.quantity

    def calculate_shipping(self, weight_kg, region="default"):
        """Рассчитывает стоимость доставки."""
        rates = {"default": 10, "express": 30, "international": 200}
        return rates.get(region, rates["default"]) / weight_kg


    def sell(self, amount):
        if amount <= 0:
            raise ValidationError(f"Количество должно быть положительным: {amount}")
        if self.quantity < amount:
            raise InsufficientStockError(
                f"Товара недостаточно. На складе: {self.quantity}, требуется: {amount}"
            )
        self.quantity -= amount
        return self.quantity

    def __str__(self):
        return f"Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}"

    def __repr__(self):
        return f"Product('{self.name}', {self.price}, {self.quantity})"

    def __lt__(self, other):
        return self.price < other.price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price
