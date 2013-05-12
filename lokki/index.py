def getNextIndex(session, class_, **filter):
  """
  filter keyword arguments are used to filter the group for which the index is
  calculated.

  If the set of indexable objects is empty, returns 1. (That is, indexes start
  from one.)
  """
  o = (session.query(class_)
              .filter_by(**filter)
              .order_by(class_.index.desc())
              .first())
  if not o:
    return 1
  else:
    return o.index + 1

