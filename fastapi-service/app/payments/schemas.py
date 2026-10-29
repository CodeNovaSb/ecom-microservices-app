from pydantic import BaseModel, Field

class PaymentCreate(BaseModel):
    order_id: int = Field(gt=0)