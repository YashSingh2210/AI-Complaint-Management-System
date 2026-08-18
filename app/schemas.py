from pydantic import BaseModel

class ComplaintCreate(BaseModel):
    customer_name: str
    email: str
    subject: str
    complaint: str
class ComplaintStatusUpdate(BaseModel):
    status: str