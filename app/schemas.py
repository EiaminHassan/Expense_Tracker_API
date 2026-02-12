from pydantic import BaseModel, EmailStr

# Datamodel for the request body
class Expense(BaseModel):
    id: int
    description: str
    amount: float
    date: str

class ExpenseResponse(Expense):
    class Config:
        orm_mode = True

# Datamodel for user creation
class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str