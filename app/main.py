from fastapi import FastAPI

from . routers import expenses, users

# Create the FastAPI app
app = FastAPI()

# Include routers
app.include_router(expenses.router)
app.include_router(users.router)