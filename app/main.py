from fastapi import Depends, FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db



app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Datamodel for the request body
class Expense(BaseModel):
    id: int
    description: str
    amount: float
    date: str

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "expenses_db"
DB_USER = "postgres"
DB_PASSWORD = "13597"

while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print(f"Database connection failed: {e}")

# endpoint to get all expenses - root endpoint
@app.get("/")
def get_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    return expenses

# endpoint to add a new expense
@app.post("/add")
def add_expense(expense: Expense):
    cursor.execute(
        "INSERT INTO expenses (id, description, amount, date) VALUES (%s, %s, %s, %s)",
        (expense.id, expense.description, expense.amount, expense.date)
    )
    conn.commit()
    return {"message": "Expense added successfully"}

# endpoint to delete an expense by id
@app.delete("/delete/{expense_id}")
def delete_expense(expense_id: int):
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    return {"message": "Expense deleted successfully"}

# endpoint to update an expense by id
@app.put("/update/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    cursor.execute(
        "UPDATE expenses SET description = %s, amount = %s, date = %s WHERE id = %s",
        (expense.description, expense.amount, expense.date, expense_id)
    )
    conn.commit()
    return {"message": "Expense updated successfully"}

# endpoint to test SQLAlchemy connection
@app.get("/expense_Alchemy")
def get_expenses_Alchemy(db: Session = Depends(get_db)):
    return {"Status": "SQLAlchemy is working!"}

# post data using SQLAlchemy
@app.post("/add_Alchemy")
def add_expense_Alchemy(expense: Expense, db: Session = Depends(get_db)):
    new_expense = models.Expense(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {"message": "Expense added successfully using SQLAlchemy"}

# get all data using SQLAlchemy
@app.get("/get_Alchemy")
def get_expenses_Alchemy(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return expenses

# get expense by id using SQLAlchemy
@app.get("/get_Alchemy/{expense_id}")
def get_expense_by_id_Alchemy(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense:
        return expense
    else:
        return {"message": f"Expense with id {expense_id} not found"}

# update expense by id using SQLAlchemy
@app.put("/update_Alchemy/{expense_id}")
def update_expense_Alchemy(expense_id: int, expense: Expense, db: Session = Depends(get_db)):
    existing_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if existing_expense:
        existing_expense.id = expense.id
        existing_expense.description = expense.description
        existing_expense.amount = expense.amount
        existing_expense.date = expense.date
        db.commit()
        return {"message": "Expense updated successfully using SQLAlchemy"}
    else:
        return {"message": f"Expense with id {expense_id} not found"}
    

