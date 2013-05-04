from lokki.db.row import Row
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
