from decimal import Decimal
from lokki.db.row import Row
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

class SimpleRow(Row):
  """
  An invoice row containing a number of units and a price per unit.
  """
  __tablename__ = 'simple_rows'

  id = Column(Integer, ForeignKey('rows.id'), primary_key=True)

  num_units = Column(String(31), nullable=False, default=1)
  price_per_unit = Column(String(31), nullable=False)

  __mapper_args__ = {
    'polymorphic_identity': 'simple',
  }

  def getTotal(self):
    return Decimal(self.price_per_unit) * Decimal(self.num_units)

  def getNumberOfUnits(self):
    return Decimal(self.num_units)

  def getPricePerUnit(self):
    return Decimal(self.price_per_unit)

