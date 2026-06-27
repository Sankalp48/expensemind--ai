# Pydantic models for validating API request and response data

from pydantic import BaseModel


# Used when creating a new expense
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str


# Used when returning expense data to the client
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str

    class Config:
        from_attributes = True