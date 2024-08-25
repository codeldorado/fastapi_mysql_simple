from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from . import models, schemas, crud, database

app = FastAPI()

# Dependency for database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=Dict)
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")

    total = db.query(models.User).count()
    users = db.query(models.User).offset(skip).limit(limit).all()
    user_list = [schemas.User.from_orm(user) for user in users]
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": user_list
    }

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(user)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    print(f"Attempting to delete user with id {user_id}")
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(deleted_user)

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_post(db=db, post=post, user_id=user_id)

@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db=db, post_id=post_id, post_update=post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

@app.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted_post = crud.delete_post(db=db, post_id=post_id)
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return deleted_post

@app.get("/posts/", response_model=Dict)
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")

    total = db.query(models.Post).count()
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    post_list = [schemas.Post.from_orm(post) for post in posts]
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": post_list
    }
