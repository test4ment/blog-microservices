from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Схемы для пользователя ---
class UserBase(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None

class UserInDB(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserInDB
    token: str

# --- Схемы для статьи ---
class ArticleBase(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = []

class ArticleCreate(ArticleBase):
    pass

class ArticleInDB(ArticleBase):
    slug: str
    author: UserInDB

    class Config:
        orm_mode = True

# --- Схемы для комментариев ---
class CommentBase(BaseModel):
    body: str

class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    id: int
    author: UserInDB

    class Config:
        orm_mode = True

# --- Схемы для JWT ---
class TokenData(BaseModel):
    username: Optional[str] = None
