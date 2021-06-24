from fastapi import APIRouter, Depends, status, HTTPException
from parking import schemas, database, models, token 
from parking.hashing import Hash
from sqlalchemy.orm import Session
import redis

router = APIRouter(tags=['Authentication'])

client = redis.Redis(host='localhost', port=6379)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.username})
    client.set(access_token, request.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.delete('/logout')
def logout(token: str):
    if client.get(token):
        client.expire(token, 1)
        return "done"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="sth went wrong")