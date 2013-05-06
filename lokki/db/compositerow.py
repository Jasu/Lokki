from lokki.db.row import Row
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

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
    return result

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
    result = Decimal(0)
    for subrow in self.subrows:
        result += Decimal(subrow.price_per_unit) * Decimal(subrow.num_units)

    return result

