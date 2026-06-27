# Import SQLAlchemy data types used to create database columns
from sqlalchemy import Column, Integer, String, Float, Date

# Import Base class from database.py
# Every database table must inherit from Base
from app.database import Base


# Expense class represents the "expenses" table in MariaDB
class Expense(Base):

    # Name of the table inside the database
    __tablename__ = "expenses"

    # Unique ID for every expense
    # primary_key=True -> Makes this the primary key
    # index=True -> Makes searching faster
    id = Column(Integer, primary_key=True, index=True)

    # Expense title
    # Example: Pizza, Netflix, Electricity Bill
    title = Column(String(100))

    # Expense amount
    # Example: 250.50, 1200.00
    amount = Column(Float)

    # Expense category
    # Example: Food, Travel, Shopping
    category = Column(String(50))

    # Date on which the expense occurred
    # Example: 2026-06-27
    date = Column(Date)