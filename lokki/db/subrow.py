from lokki.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

class Subrow(Base):
  """
  A subrow of a CompositeRow.
  """
  __tablename__ = 'sub_rows'

  id = Column(Integer, primary_key=True)

  description = Column(String(255), nullable=False)
  note = Column(String(511))
  ordering = Column(Integer, nullable=False)

  external_source = Column(String(63), nullable=False, default='lk')
  external_id = Column(String(255), nullable=True)

  num_units = Column(String(31), nullable=False, default=1)
  price_per_unit = Column(String(31), nullable=False)

  row_id = Column(Integer, ForeignKey('composite_rows.id'), nullable=False)
  row = relationship('CompositeRow', backref=backref('sub_rows', order_by=ordering))

