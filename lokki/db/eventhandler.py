from lokki.db.base import Base

from sqlalchemy import Column, Integer, String

class EventHandler(Base):
  __tablename__ = 'event_handlers'
  id = Column(Integer, primary_key=True)
  index = Column(Integer)
  event = Column(String(31), nullable=False)
  command = Column(String(255), nullable=False)

