# Import SQLAlchemy data types used to create database columns
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

# Import Base class from database.py
# Every database table must inherit from Base
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    amount = Column(Float)
    category = Column(String(50))
    date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id"))