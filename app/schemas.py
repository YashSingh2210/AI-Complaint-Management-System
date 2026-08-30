from pydantic import BaseModel,ConfigDict,Field,EmailStr
from datetime import datetime

class ComplaintCreate(BaseModel):
    customer_name: str = Field(min_length=2)
    email: EmailStr
    subject: str = Field(min_length=5)
    complaint: str = Field(min_length=20)
class ComplaintStatusUpdate(BaseModel):
    status: str
class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    role: str = "user"
class UserLogin(BaseModel):
    username: str
    password: str
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class ComplaintResponse(BaseModel):
    id: int
    customer_name: str
    email: str
    subject: str
    complaint: str
    category: str
    priority: str
    status: str
    ai_reply: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)