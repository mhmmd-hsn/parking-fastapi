from sqlalchemy.orm import Session
from parking import models, schemas
from fastapi import HTTPException, status
from parking.hashing import Hash


def create(request: schemas.User, db: Session):
    new_user = models.User(
        username=request.username,password=Hash.bcrypt(request.password),is_admin = request.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user
