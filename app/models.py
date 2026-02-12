from psycopg2 import Timestamp
from sqlalchemy import Column, Integer, String, Float, Date, func
from .database import Base


# SQLAlchemy model for the Expense table
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

# SQLAlchemy model for the User table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    user_name = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)