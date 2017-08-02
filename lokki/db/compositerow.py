from lokki.db.row import Row
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from math import ceil

class CompositeRow(Row):
  """
  An invoice row containing a number of sub rows, not printed on the invoice.
  """
  __tablename__ = 'composite_rows'

  id = Column(Integer, ForeignKey('rows.id'), primary_key=True)

  __mapper_args__ = {
    'polymorphic_identity': 'composite',
  }

  def getNumberOfUnits(self):
    result = Decimal(0)
    for subrow in self.subrows:
      result += Decimal(subrow.num_units)
    return Decimal(ceil(result))

  def getPricePerUnit(self):
    """
    If different subrows have different prices, returns None.
    """
    result = None
    for subrow in self.subrows:
      if result == None:
        result = Decimal(subrow.price_per_unit)
      elif result != Decimal(subrow.price_per_unit):
        return None

    return result

  def getTotal(self):
    if len(self.subrows) < 0:
      return 0
    units = Decimal(0)
    price_per_unit = Decimal(0)
    for subrow in self.subrows:
        units += Decimal(subrow.num_units)
        price_per_unit = subrow.price_per_unit
    return Decimal(price_per_unit) * ceil(units)

