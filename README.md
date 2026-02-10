# Expense Tracker API (Learning Project)

Basically I am learning FastAPI and doing hands-on work through this project.

## What it does

- Simple CRUD API for expenses
- Uses PostgreSQL for storage
- Includes a small SQLAlchemy smoke-test route

## Endpoints

- GET / - list expenses
- POST /add - create expense
- PUT /update/{expense_id} - update expense
- DELETE /delete/{expense_id} - delete expense
- GET /expense_Alchemy - SQLAlchemy check

## Requirements

- Python 3.10+
- PostgreSQL running locally
- Packages: fastapi, uvicorn, psycopg2, sqlalchemy, pydantic

## Quick start

1. Create a Postgres database named expenses_db
2. Update credentials in app/main.py and app/database.py if needed
3. Install dependencies
4. Run the app

Example run:

- fastapi dev app/main.py

## Notes

- Tables are created on startup via SQLAlchemy.
- The Expense model has: id, description, amount, date.
