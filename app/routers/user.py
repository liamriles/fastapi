from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found.")
    return user

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password from user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{id}")
def delete_user(id: int, status_code=status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist.")
    
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, status_code=status.HTTP_202_ACCEPTED, db: Session = Depends(get_db)):
    # hash the password from user.password
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist.")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user_query.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()

    return user_query.first()