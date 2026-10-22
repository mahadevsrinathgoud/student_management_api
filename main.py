
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management REST API")


@app.get("/")
def home():
    return {"message": "Student Management API is running"}


# 1. Register a student
@app.post(
    "/students/",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = models.Student(**student.model_dump())

    db.add(new_student)

    try:
        db.commit()
        db.refresh(new_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return new_student


# 2. Get all students
@app.get("/students/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


# 3. Get a student by ID
@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# 4. Update a student
@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    updated_data: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    for field, value in updated_data.model_dump().items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered by another student"
        )

    return student


# 5. Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
