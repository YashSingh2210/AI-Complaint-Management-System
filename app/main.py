from fastapi import FastAPI,Depends,HTTPException
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session
from .schemas import ComplaintCreate,ComplaintStatusUpdate
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

# get complaints by_id.
@app.get("/complaints/{complaint_id}")
def get_complaint_by_id(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )
    return complaint

 # complaint status update
@app.put("/complaints/{complaint_id}")
def update_complaint_status(
    complaint_id: int,
    update: ComplaintStatusUpdate,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )
    complaint.status = update.status
    db.commit()
    db.refresh(complaint)
    return {
        "message": "Complaint status updated successfully",
        "complaint": complaint
    }

# deletion of complaint
@app.delete("/complaints/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )
    db.delete(complaint)
    db.commit()
    return {
        "message": "Complaint deleted successfully"
    }