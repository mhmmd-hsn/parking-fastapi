from fastapi import FastAPI
from parking import  models
from parking.database import engine
from parking.routers import  user,authentication,slot

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(slot.router)