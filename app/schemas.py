from pydantic import BaseModel, EmailStr, constr, validator
from typing import List
import re


'''
Post Schemas
'''
class PostBase(BaseModel):
    title: constr(min_length=5, max_length=100)
    content: constr(min_length=10, max_length=1000)

    @validator('title')
    def no_whitespace_only(cls, value):
        if value.strip() == "":
            raise ValueError("title cannot be just whitespace")
        return value

    @validator('content')
    def sanitize_content(cls, value):
        if "<script>" in value.lower():
            raise ValueError("content cannot contain script tags")
        return value

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True

'''
User Schemas
'''
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

    @validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError("Username must contain only alphanumeric characters and underscores.")
        if value.strip() == "":
            raise ValueError("Username cannot be just whitespace")
        return value

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=100)

    @validator('password')
    def password_strength(cls, value):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', value):
            raise ValueError("Password must contain at least one letter and one number")
        return value

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

'''
Schema for user with posts
'''
class UserWithPosts(User):
    posts: List[Post] = []
