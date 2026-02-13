from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_db

router = APIRouter()

# endpoint to test SQLAlchemy connection
@router.get("/expense_Alchemy")
def get_expenses_Alchemy(db: Session = Depends(get_db)):
    return {"Status": "SQLAlchemy is working!"}

# post data using SQLAlchemy
@router.post("/add_Alchemy", response_model=schemas.ExpenseResponse)
def add_expense_Alchemy(expense: schemas.Expense, db: Session = Depends(get_db)):
    new_expense = models.Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# get all data using SQLAlchemy
@router.get("/get_Alchemy", response_model=list[schemas.ExpenseResponse])
def get_expenses_Alchemy(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return expenses

# get expense by id using SQLAlchemy
@router.get("/get_Alchemy/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense_by_id_Alchemy(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense:
        return expense
    else:
        return {"message": f"Expense with id {expense_id} not found"}

# update expense by id using SQLAlchemy
@router.put("/update_Alchemy/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense_Alchemy(expense_id: int, expense: schemas.Expense, db: Session = Depends(get_db)):
    existing_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if existing_expense:
        existing_expense.id = expense.id
        existing_expense.description = expense.description
        existing_expense.amount = expense.amount
        existing_expense.date = expense.date
        db.commit()
        db.refresh(existing_expense)
        return existing_expense
    else:
        return {"message": f"Expense with id {expense_id} not found"}
    

# delete expense by id using SQLAlchemy
@router.delete("/delete_Alchemy/{expense_id}")
def delete_expense_Alchemy(expense_id: int, db: Session = Depends(get_db)):
    existing_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if existing_expense:
        db.delete(existing_expense)
        db.commit()
        return {"message": "Expense deleted successfully using SQLAlchemy"}
    else:
        return {"message": f"Expense with id {expense_id} not found"}