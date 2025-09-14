from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Product
from app.exceptions import OutOfStockException, ProductNotFoundException, OrderNotFoundException


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_item(db: Session, order_id: int, product_id: int):
    return db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.product_id == product_id
    ).first()


def add_item_to_order(db: Session, order_id: int, product_id: int, quantity: int):
    # Проверяем существование заказа
    order = get_order(db, order_id)
    if not order:
        raise OrderNotFoundException(order_id)

    # Проверяем существование товара
    product = get_product(db, product_id)
    if not product:
        raise ProductNotFoundException(product_id)

    # Проверяем наличие товара на складе
    if product.stock_quantity < quantity:
        raise OutOfStockException(product_id, quantity, product.stock_quantity)

    # Ищем существующую позицию в заказе
    existing_item = get_order_item(db, order_id, product_id)

    if existing_item:
        # Обновляем количество существующей позиции
        existing_item.quantity += quantity
        item = existing_item
    else:
        # Создаем новую позицию
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.add(item)

    # Обновляем количество товара на складе
    product.stock_quantity -= quantity

    # Обновляем общую сумму заказа
    order.total_amount += product.price * quantity

    db.commit()
    db.refresh(item)

    return item