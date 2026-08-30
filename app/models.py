from sqlalchemy import Column, Integer, String,Text,DateTime, ForeignKey
from .database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_name = Column(String)
    email = Column(String)
    subject = Column(String)
    complaint = Column(String)
    category = Column(String, default="Other")
    priority = Column(String)
    ai_reply = Column(Text)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
    DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)
    resolved_at = Column(DateTime, nullable=True)
    
    owner = relationship("User", back_populates="complaints")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    role = Column(String, default="user")
    complaints = relationship("Complaint", back_populates="owner")

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

