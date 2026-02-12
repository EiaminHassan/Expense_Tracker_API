from pydantic import BaseModel, EmailStr

# Datamodel for the request body
class Expense(BaseModel):
    id: int
    description: str
    amount: float
    date: str

# Datamodel for the Expenses response body
class ExpenseResponse(Expense):
    class Config:
        orm_mode = True

# Datamodel for user creation
class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str