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

# User Schemas

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True        