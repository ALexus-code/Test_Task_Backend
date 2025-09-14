from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, exceptions
from app.database import get_db, init_db

app = FastAPI(
    title="Order Service API",
    description="Сервис для добавления товаров в заказ",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.post(
    "/orders/{order_id}/items",
    response_model=schemas.OrderItemResponse,
    responses={
        400: {"model": schemas.ErrorResponse, "description": "Недостаточно товара на складе"},
        404: {"model": schemas.ErrorResponse, "description": "Заказ или товар не найден"}
    }
)
async def add_item_to_order(
        request: schemas.AddItemRequest,
        db: Session = Depends(get_db)
):
    """
    Добавить товар в заказ.

    - Если товар уже есть в заказе, увеличивает его количество
    - Проверяет наличие товара на складе
    - Возвращает ошибку если товара недостаточно
    """
    try:
        order_item = crud.add_item_to_order(
            db=db,
            order_id=request.order_id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        return order_item

    except exceptions.OutOfStockException as e:
        raise HTTPException(status_code=400, detail=str(e))

    except (exceptions.ProductNotFoundException, exceptions.OrderNotFoundException) as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}