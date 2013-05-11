from lokki.db.base import Base
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Column, Integer, String

class Client(Base):
  __tablename__ = 'clients'

  id = Column(Integer, primary_key=True, nullable=False)
  handle = Column(String(63), nullable=False, unique=True)
  client_number = Column(Integer)
  name = Column(String(127))
  address = Column(String(127))
  address_2 = Column(String(127))
  zip_code = Column(String(15))
  city = Column(String(63))
  country = Column(String(63))
  company_number = Column(String(63))
  vat_number = Column(String(63))

  def isValid(self):
    if (not self.name or not self.name.strip()):
      return False

    if (not self.address or not self.address.strip()):
      return False

    if (not self.zip_code or not self.zip_code.strip()):
      return False

    if (not self.city or not self.city.strip()):
      return False

    if (not self.country or not self.country.strip()):
      return False

    return True

