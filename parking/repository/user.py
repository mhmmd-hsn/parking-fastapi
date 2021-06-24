from sqlalchemy.orm import Session
from parking import models, schemas
from fastapi import HTTPException, status
from parking.hashing import Hash
from parking.routers import authentication
from elasticsearch import Elasticsearch
import psycopg2

con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="19a82b37c")

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='parking_data_user', ignore=400)
cur = con.cursor()


def create(request: schemas.User, db: Session):
    cur.execute("insert into users (username,password,is_admin) values (%s, %s,%s)", (request.username,
                                                                                      Hash.bcrypt(request.password),
                                                                                      request.is_admin))
    con.commit()
    elastic = {
        "username": request.username,
        "password": Hash.bcrypt(request.password),
        "is_admin": request.is_admin
    }
    es.index(index='parking_data_user', doc_type='user', body=elastic)
    if request.is_admin:
        authentication.client.set(request.username, "true")
    return 'user added'


def show(id: int):
    cur.execute("select * from users where id = %s", (id,))
    user = cur.fetchall()
    return user


def update(id: int, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    request.password = Hash.bcrypt(request.password)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with user {id} not found")
    user.update(request)
    db.commit()
    return 'updated'


def destroy(id: int):
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    con.commit()
    return 'done'
