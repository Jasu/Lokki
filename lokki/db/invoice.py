from lokki.db.base import Base

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

class Invoice(Base):
  __tablename__ = 'invoices'

  id = Column(Integer, primary_key=True)
  invoice_number = Column(Integer, unique=True, nullable=False)

  time_added = Column(DateTime, nullable=False)

  date = Column(Date, nullable=False)
  due_date = Column(Date, nullable=False)

  reference = Column(Integer, unique=True, nullable=False)

  is_billed = Column(Boolean, nullable=False, default=False)

  client_id = Column(Integer, ForeignKey('clients.id'))
  client = relationship('Client', backref=backref('invoices', order_by=date))

  # Sender data, copied from settings, to make the bill look the same if it is
  # regenerated.

  seller_name = Column(String(255), nullable=False)
  seller_address = Column(String(255), nullable=False)
  seller_address_2 = Column(String(255))
  seller_zip_code = Column(String(255), nullable=False)
  seller_city = Column(String(255), nullable=False)
  seller_country = Column(String(255))
  seller_phone_number = Column(String(255))
  seller_company_number = Column(String(255))
  seller_vat_number = Column(String(255))
  seller_iban = Column(String(255), nullable=False)

  # Client data, copied from client, to make the bull look the same if it is
  # regenerated.

  client_name = Column(String(127), nullable=False)
  client_number = Column(Integer, nullable=False)
  client_address = Column(String(127), nullable=False)
  client_address_2 = Column(String(127))
  client_zip_code = Column(String(15), nullable=False)
  client_city = Column(String(63), nullable=False)
  client_country = Column(String(63))

