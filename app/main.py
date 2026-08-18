from fastapi import FastAPI,Depends
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session
from .schemas import ComplaintCreate
from .models import Complaint
print("Creating Database...")
models.Base.metadata.create_all(bind=engine)
app=FastAPI()
@app.get("/")
def home():
    return{"message":"ResolveAI backend is running"}

@app.post("/complaints")
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db) # ask from api a new database connection
):
    new_complaint = Complaint(
        customer_name=complaint.customer_name,
        email=complaint.email,
        subject=complaint.subject,
        complaint=complaint.complaint
    )
    db.add(new_complaint) # register new complain
    db.commit()# save the complain
    db.refresh(new_complaint)
    return {
        "message": "Complaint submitted successfully",
        "id": new_complaint.id
    }

# getting all complains from database.
@app.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).all()# start/perform query on complaint table
    return complaints