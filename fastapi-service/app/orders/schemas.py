from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    user_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    status: str
    created_at: datetime
