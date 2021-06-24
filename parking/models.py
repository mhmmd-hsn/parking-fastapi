from sqlalchemy import Column, Integer, String, Boolean
from parking.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, default=False)


class Slot(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    happened_at = Column(String)
    slot_num = Column(Integer)
    event_type = Column(String)


