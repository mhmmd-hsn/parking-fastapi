from sqlalchemy.orm import Session
from parking import models
from fastapi import HTTPException, status
from parking.routers import authentication
from datetime import datetime
from parking.repository import user

user.es.indices.create(index='parking_data', ignore=400)


def enter_event(token: str, db: Session):
    username = authentication.client.get(token)
    if username:
        username = str(authentication.client.get(token))
        username = username[2:-1]
        check = db.query(models.Slot).filter(models.Slot.username == username).order_by(models.Slot.id.desc()).first()
        if not check or check.event_type == 'exit':
            event_time = datetime.utcnow()
            capacity = int(authentication.client.get('capacity'))
            for i in range(1, capacity):
                slot_activities = db.query(models.Slot).filter(models.Slot.slot_num == i).count()
                x = slot_activities % 2
                if x == 0:
                    slot_number = i
                    break
                if i == capacity:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="parking is full !!!")

            elastic = {
                "username": username,
                "happened_at": event_time,
                "slot_num": slot_number,
                "event_type": "enter"
            }
            user.es.index(index='parking_data', doc_type='slot', body=elastic)
            slot_inf = models.Slot(username=username, happened_at=event_time,
                                   slot_num=slot_number, event_type='enter')
            db.add(slot_inf)
            db.commit()
            db.refresh(slot_inf)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You are already in !!!")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You are not authenticated!!")

    return slot_inf


def update(extra: int, token: str):
    username = authentication.client.get(token)
    if username:
        username = str(authentication.client.get(token))
        username = username[2:-1]
        if authentication.client.get(username):
            past_capacity = int(authentication.client.get('capacity'))
            latest_capacity = extra + past_capacity
            authentication.client.set('capacity', latest_capacity)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Sorry,You are not allowed!!")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You are not authenticated!!")
    return 'its done'


def exit_event(token: str, db: Session):
    username = authentication.client.get(token)
    if username:
        username = str(authentication.client.get(token))
        username = username[2:-1]
        check = db.query(models.Slot).filter(models.Slot.username == username).order_by(models.Slot.id.desc()).first()
        if check.event_type == 'enter':
            event_time = datetime.utcnow()
            slot_inf = models.Slot(username=username, happened_at=event_time,
                                   slot_num=check.slot_num, event_type='exit')
            elastic = {
                "username": username,
                "happened_at": event_time,
                "slot_num": check.slot_num,
                "event_type": "exit"
            }
            user.es.index(index='parking_data', doc_type='slot', body=elastic)
            db.add(slot_inf)
            db.commit()
            db.refresh(slot_inf)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="you are already out !!!!")
    return 'this slot is empty now.'


def all_data(token: str, db: Session):
    username = authentication.client.get(token)
    if username:
        username = str(authentication.client.get(token))
        username = username[2:-1]
        if authentication.client.get(username):
            all_slots = db.query(models.Slot).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="u are not allowed")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You are not authenticated!!")
    return all_slots


def elastic_query():
    free_slots = []
    for i in range(1, int(authentication.client.get('capacity'))+1):
        res = user.es.search(index='parking_data', body={'query': {'match': {'slot_num': i}}})
        x = res["hits"]["total"]["value"]
        if x % 2 == 0:
            free_slots.append(i)
    return free_slots
