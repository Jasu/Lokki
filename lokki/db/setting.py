from lokki.db.base import Base

from sqlalchemy import Column, Integer, String

class Setting(Base):
  __tablename__ = 'settings'
  name = Column(String(31), primary_key=True, nullable=False)
  value = Column(String(255), nullable=False)

