from fastapi import FastAPI , HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# Request Model
class UserRegister(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(ge=18)
    city: str = "Delhi"
    
# Response model
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    city: str
    
# Temporary database
users = []

# 3. Register Endpoint
@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserRegister):
    
    # new_id = len(users) + 1
    
    new_id = max(
    (user["id"] for user in users),
    default=0
) + 1
    
    new_user = {
        "id": new_id, 
        **user.model_dump()
    }
    
    users.append(new_user)
    
    return new_user
    
# 4. Get all users endpoint
@app.get("/users", response_model=list[UserResponse])
def get_users():
    return users
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )