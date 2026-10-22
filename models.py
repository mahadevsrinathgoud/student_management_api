
from sqlalchemy import Column, Integer, String, Float
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String(100), nullable=False)
    marks = Column(Float, nullable=False)
