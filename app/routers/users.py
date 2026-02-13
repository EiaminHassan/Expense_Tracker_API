from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from .. import models, utilis, schemas
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




# create user using SQLAlchemy
@router.post("/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utilis.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get all users using SQLAlchemy
@router.get("/", response_model=list[schemas.UserCreate])
def get_users_Alchemy(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users