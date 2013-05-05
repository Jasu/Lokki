
from lokki.db.base import Base

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

class Row(Base):
  __tablename__ = 'rows'

  id = Column(Integer, primary_key=True)

  type = Column(String(16))

  title = Column(String(255), nullable=False)
  note = Column(String(511))
  vat = Column(String(31), nullable=False)
  index = Column(Integer, nullable=False)

  external_source = Column(String(63), nullable=False, default='lk')
  external_id = Column(String(255), nullable=True)

  invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
  invoice = relationship('Invoice', backref=backref('rows', order_by=index))

  __mapper_args__ = {
    'polymorphic_identity': 'row',
    'polymorphic_on':type,
  }
  
  def getTotal(self):
    """
    Gets the total price.
    """
    dieIf(True, "getTotal not implemented.")

  def getNumberOfUnits(self):
    """
    Gets the total number of units, even if the units do not 
    have the same price.
    """
    dieIf(True, "getNumberOfUnits not implemented.")

  def getPricePerUnit(self):
    """
    Gets the price of unit, if the price of all units is equal.
    Otherwise, returns None.
    """
    dieIf(True, "getNumberOfUnits not implemented.")

