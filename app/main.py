from fastapi import FastAPI,Depends,HTTPException
from .database import engine,get_db
from . import models
from sqlalchemy.orm import Session
from .schemas import ComplaintCreate,ComplaintStatusUpdate,UserCreate,UserLogin,UserResponse
from .models import Complaint,User
from .ai_service import get_category,get_priority,generate_reply, generate_status_reply
from datetime import datetime
from sqlalchemy import func
from .hashing import hash, verify
from .auth import create_access_token,get_current_user,admin_only
from fastapi.security import OAuth2PasswordRequestForm
print("Creating Database...")
models.Base.metadata.create_all(bind=engine)
app=FastAPI()
@app.get("/")
def home():
    return{"message":"ResolveAI backend is running"}

@app.post("/complaints")
def create_complaint(
    complaint: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db) # ask from api a new database connection
    
):
    category = get_category(complaint.complaint)
    priority = get_priority(complaint.complaint)
    reply = generate_reply(complaint.customer_name,complaint.complaint)
    new_complaint = Complaint(
        customer_name=complaint.customer_name,
        email=complaint.email,
        subject=complaint.subject,
        complaint=complaint.complaint,
        category=category,
        priority=priority,
        status="Pending",
        ai_reply=reply,
        user_id=current_user.id
    )
    db.add(new_complaint) # register new complain
    db.commit()# save the complain
    db.refresh(new_complaint)
    return {
        "message": "Complaint submitted successfully",
    "complaint": {
        "id": new_complaint.id,
        "customer_name": new_complaint.customer_name,
        "email": new_complaint.email,
        "subject": new_complaint.subject,
        "complaint": new_complaint.complaint,
        "category": new_complaint.category,
        "priority": new_complaint.priority,
        "status": new_complaint.status,
        "ai_reply": new_complaint.ai_reply,
    }
    }

# getting all complains from database.(all complaints)
# @app.get("/complaints")
# def get_complaints(db: Session = Depends(get_db)):
#     complaints = db.query(Complaint).all()# start/perform query on complaint table
#     return complaints

# only limited complaints:-
@app.get("/complaints")
def get_complaints(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    complaints = (
        db.query(Complaint)
        .offset(skip)
        .limit(limit)
        .all()
    )
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
    current_user: User = Depends(get_current_user),
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
    if (
    current_user.role != "admin"
    and complaint.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
    )
    complaint.status = update.status.title()
    if update.status.lower() == "resolved":
          complaint.resolved_at = datetime.utcnow()
    complaint.ai_reply = generate_status_reply(
    complaint.customer_name,
    complaint.complaint,
    complaint.status
)
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
    current_user: User = Depends(get_current_user),
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
    if (
    current_user.role != "admin"
    and complaint.user_id != current_user.id
):
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
    )
    db.delete(complaint)
    db.commit()
    return {
        "message": "Complaint deleted successfully"
    }

# dashboard:-
@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total = db.query(Complaint).count()

    pending = db.query(Complaint).filter(
        Complaint.status == "Pending"
    ).count()

    resolved = db.query(Complaint).filter(
        Complaint.status == "Resolved"
    ).count()

    high_priority = db.query(Complaint).filter(
        Complaint.priority == "High"
    ).count()

    return {
        "total": total,
        "pending": pending,
        "resolved": resolved,
        "high_priority": high_priority
    }

# search by customer name:-
@app.get("/search")
def search_complaints(
    name: str,
    db: Session = Depends(get_db)
):

    complaints = db.query(Complaint).filter(
        Complaint.customer_name.ilike(f"%{name}%")
    ).all()
    return complaints

# filter by status:-
@app.get("/complaints/status/{status}")
def filter_status(
    status: str,
    db: Session = Depends(get_db)
):

    complaints = db.query(Complaint).filter(
        Complaint.status == status.title()
    ).all()
    return complaints

# filter by priority:-
@app.get("/complaints/priority/{priority}")
def filter_priority(
    priority: str,
    db: Session = Depends(get_db)
):
    complaints = db.query(Complaint).filter(
        Complaint.priority == priority.title()
    ).all()

    return complaints

# filter by category:-
@app.get("/complaints/category/{category}")
def filter_category(
    category: str,
    db: Session = Depends(get_db)
):
    complaints = db.query(Complaint).filter(
        Complaint.category == category.title()
    ).all()

    return complaints

# category analytics:-
@app.get("/analytics/category")
def analytics_category(db: Session = Depends(get_db)):
    result = (
        db.query(
            Complaint.category,
            func.count(Complaint.id)
        )
        .group_by(Complaint.category)
        .all()
    )
    return [
        {
            "category": category,
            "total": total
        }
        for category, total in result
    ]

# priority analytics:-
@app.get("/analytics/priority")
def analytics_priority(
    db: Session = Depends(get_db)
):

    result = (
        db.query(
            Complaint.priority,
            func.count(Complaint.id)
        )
        .group_by(Complaint.priority)
        .all()
    )
    summary = {
    "High": 0,
    "Medium": 0,
    "Low": 0
}
    for priority, count in result:
            summary[priority] = count
    return summary

#signup API:-
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }

#login API:-
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == form_data.username
    ).first()
    if not db_user:
        return {"message": "Invalid Username"}
    if not verify(form_data.password, db_user.password):
        return {"message": "Invalid Password"}
    token = create_access_token(
        {"sub": db_user.username}
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/admin")
def admin_dashboard(
    current_user: User = Depends(admin_only)
):
    return {
        "message":"Welcome Admin"
    }

@app.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return {
         "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

#My Complaints API:-
@app.get("/my-complaints")
def my_complaints(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaints = db.query(Complaint).filter(
        Complaint.user_id == current_user.id
    ).all()

    return complaints

# admin all complaints:-
@app.get("/all-complaints")
def all_complaints(
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    return db.query(Complaint).all()