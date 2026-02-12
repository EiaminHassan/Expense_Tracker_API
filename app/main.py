from fastapi import Depends, FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utilis
from sqlalchemy.orm import Session
from .database import engine, get_db


# Create the FastAPI app
app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)



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
# @app.get("/")
# def get_expenses():
#     cursor.execute("SELECT * FROM expenses")
#     expenses = cursor.fetchall()
#     return expenses

# # endpoint to add a new expense
# @app.post("/add")
# def add_expense(expense: schemas.Expense):
#     cursor.execute(
#         "INSERT INTO expenses (id, description, amount, date) VALUES (%s, %s, %s, %s)",
#         (expense.id, expense.description, expense.amount, expense.date)
#     )
#     conn.commit()
#     return {"message": "Expense added successfully"}

# # endpoint to delete an expense by id
# @app.delete("/delete/{expense_id}")
# def delete_expense(expense_id: int):
#     cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
#     conn.commit()
#     return {"message": "Expense deleted successfully"}

# # endpoint to update an expense by id
# @app.put("/update/{expense_id}")
# def update_expense(expense_id: int, expense: schemas.Expense):
#     cursor.execute(
#         "UPDATE expenses SET description = %s, amount = %s, date = %s WHERE id = %s",
#         (expense.description, expense.amount, expense.date, expense_id)
#     )
#     conn.commit()
#     return {"message": "Expense updated successfully"}

# endpoint to test SQLAlchemy connection
@app.get("/expense_Alchemy")
def get_expenses_Alchemy(db: Session = Depends(get_db)):
    return {"Status": "SQLAlchemy is working!"}

# post data using SQLAlchemy
@app.post("/add_Alchemy", response_model=schemas.ExpenseResponse)
def add_expense_Alchemy(expense: schemas.Expense, db: Session = Depends(get_db)):
    new_expense = models.Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# get all data using SQLAlchemy
@app.get("/get_Alchemy", response_model=list[schemas.ExpenseResponse])
def get_expenses_Alchemy(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return expenses

# get expense by id using SQLAlchemy
@app.get("/get_Alchemy/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense_by_id_Alchemy(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense:
        return expense
    else:
        return {"message": f"Expense with id {expense_id} not found"}

# update expense by id using SQLAlchemy
@app.put("/update_Alchemy/{expense_id}", response_model=schemas.ExpenseResponse)
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
@app.delete("/delete_Alchemy/{expense_id}")
def delete_expense_Alchemy(expense_id: int, db: Session = Depends(get_db)):
    existing_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if existing_expense:
        db.delete(existing_expense)
        db.commit()
        return {"message": "Expense deleted successfully using SQLAlchemy"}
    else:
        return {"message": f"Expense with id {expense_id} not found"}

# create user using SQLAlchemy
@app.post("/user_Alchemy", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utilis.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user