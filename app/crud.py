from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_user(db: Session, user_id: int, user_update: schemas.UserCreate):
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    db_user.username = user_update.username
    db_user.email = user_update.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def update_post(db: Session, post_id: int, post_update: schemas.PostCreate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None
    db_post.title = post_update.title
    db_post.content = post_update.content
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()
    return db_post
