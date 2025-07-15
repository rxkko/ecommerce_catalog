from pydantic import BaseModel


class OrderResponse(BaseModel):
    order_id: int
    
    class Config:
        from_attributes = True