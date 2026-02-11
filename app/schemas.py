from pydantic import BaseModel

# Datamodel for the request body
class Expense(BaseModel):
    id: int
    description: str
    amount: float
    date: str

class ExpenseResponse(Expense):
    class Config:
        orm_mode = True