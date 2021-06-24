from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    username:str
    password:str
    is_admin:bool
 

class ShowUser(BaseModel):

    username:str
    is_admin:str
    
    class Config():
        orm_mode = True

class Slot(BaseModel):
    username  : str
    happend_at: str
    slot_num  : int
    event_type: str

class ShowSlot(BaseModel):
    username  : str
    happened_at: str
    slot_num  : int
    
    class Config():
        orm_mode = True


class Slot_enter(BaseModel):
    username  : str

class Slot_exit(BaseModel):
    username  : str
    slot_num  : int