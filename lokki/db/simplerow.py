from lokki.db.row import Row
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref

class SimpleRow(Row):
  """
  An invoice row containing a number of units and a price per unit.
  """
  __tablename__ = 'simple_rows'

  id = Column(Integer, ForeignKey('rows.id'), primary_key=True)

  num_units = Column(Numeric(precision=10, scale=5), nullable=False, default=1)
  price_per_unit = Column(Numeric(precision=15, scale=5), nullable=False)

  __mapper_args__ = {
    'polymorphic_identity': 'simple',
  }
