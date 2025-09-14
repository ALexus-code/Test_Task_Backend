from pydantic import BaseModel, Field
from typing import Optional

class AddItemRequest(BaseModel):
    order_id: int = Field(..., gt=0, description="ID заказа")
    product_id: int = Field(..., gt=0, description="ID товара")
    quantity: int = Field(..., gt=0, description="Количество товара")

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    detail: str