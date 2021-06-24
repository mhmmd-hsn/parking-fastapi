from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from parking import schemas, database, models
from sqlalchemy.orm import Session
from parking.repository import slot
import datetime


router = APIRouter(
    prefix="/slot",
    tags=['slot']
)

get_db = database.get_db

slot_number = 0
car_slots = [0,0,0]


@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schemas.ShowSlot)
def enter(request: schemas.Slot_enter, db: Session = Depends(get_db)):
    return slot.enter_car(request, db)


@router.put('slot/update',status_code=status.HTTP_202_ACCEPTED)
def update(extra : int):
    for i in range(extra):
        car_slots.append(0)
    return 'done' 

@router.get('/',response_model = schemas.ShowSlot)
def all_events(db :Session = Depends(get_db)):
    all_slots = db.query(models.Slot).all()
    return all_slots 


@router.delete('/exit',status_code=status.HTTP_204_NO_CONTENT)
def exit (request : schemas.Slot_exit,db :Session = Depends(get_db)):
    if car_slots[request.slot_num-1] == 1:
         car_slots[request.slot_num-1] = 0
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="there is no car in this slot") 

    slot_inf = models.Slot(username=request.username, happened_at=str(datetime.datetime.now()),
                            slot_number = request.slot_num,event_type ='exit')
    db.add(slot_inf)
    db.commit()
    db.refresh(slot_inf)

    return {f'slot num{request.slot_num}is empty now.'}