from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

# User Schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


class userLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Post schemas

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True
    

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True

# Vote schemas

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]