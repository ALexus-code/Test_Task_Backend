class OutOfStockException(Exception):
    def __init__(self, product_id: int, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(f"Недостаточно товара {product_id}. Запрошено: {requested}, доступно: {available}")

class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Товар {product_id} не найден")

class OrderNotFoundException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Заказ {order_id} не найден")