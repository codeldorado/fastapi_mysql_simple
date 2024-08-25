from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    posts = relationship('Post', back_populates='owner')

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, server_default=func.now())
    
    owner = relationship('User', back_populates='posts')
