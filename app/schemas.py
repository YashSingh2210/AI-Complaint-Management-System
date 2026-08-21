from pydantic import BaseModel,ConfigDict

class ComplaintCreate(BaseModel):
    customer_name: str
    email: str
    subject: str
    complaint: str
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