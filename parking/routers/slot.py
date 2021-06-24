from typing import List
from fastapi import APIRouter, Depends, status
from parking import schemas, database
from sqlalchemy.orm import Session
from parking.repository import slot


get_db = database.get_db

router = APIRouter(
    prefix="/slot",
    tags=['slot']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowSlot)
def enter_car(token: str, db: Session = Depends(get_db)):
    return slot.enter_event(token, db)


@router.delete('/exit', status_code=status.HTTP_204_NO_CONTENT)
def exit_car(token: str, db: Session = Depends(get_db)):
    return slot.exit_event(token, db)


@router.get('/all_events', response_model=List[schemas.ShowSlot])
def all_events(token: str, db: Session = Depends(get_db)):
    return slot.all_data(token, db)


@router.put('/update', status_code=status.HTTP_202_ACCEPTED)
def update_capasity(extra: int, token: str):
    return slot.update(extra, token)


@router.get('/elasticquery')
def present_data():
    return slot.elastic_query()
