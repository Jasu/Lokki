from lokki.db.base import Base

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship, backref

class Row(Base):
  __tablename__ = 'rows'

  id = Column(Integer, primary_key=True)

  type = Column(String(16))

  description = Column(String(255), nullable=False)
  note = Column(String(511))
  vat = Column(Numeric(precision=4,scale=3), nullable=False)
  ordering = Column(Integer, nullable=False)

  source = Column(String(63), nullable=False, default='lk')
  external_id = Column(String(255), nullable=True)

  invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
  invoice = relationship('Invoice', backref=backref('rows', order_by=ordering))

  __mapper_args__ = {
    'polymorphic_identity': 'row',
    'polymorphic_on':type,
  }
