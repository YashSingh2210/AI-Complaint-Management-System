from sqlalchemy import Column, Integer, String
from .database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    email = Column(String)
    subject = Column(String)
    complaint = Column(String)
    status = Column(String, default="Pending")