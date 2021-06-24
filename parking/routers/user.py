from parking import database, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from parking.repository import user


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return user.update(id, request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return user.destroy(id, db)

