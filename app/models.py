from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


# SQLAlchemy model for the Expense table
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    date = Column(String, nullable=False)