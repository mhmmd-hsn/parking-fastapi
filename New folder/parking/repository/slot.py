from sqlalchemy.orm import Session
from parking import models, schemas
from fastapi import HTTPException, status


def enter_car (request: schemas.Slot_enter, db: Session):
    for i in range(3):
        if car_slots[i] == 0: 
            car_slots[i] = 1
            slot_number=i+1
            break
        else:
            slot_number = 0
    
    if slot_number != 0 :
        slot_inf = models.Slot(username=request.username, happened_at =str(datetime.datetime.now()),
                               slot_num = slot_number,event_type ='enter')
        db.add(slot_inf)
        db.commit()
        db.refresh(slot_inf)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="parking is full")
    return slot_inf