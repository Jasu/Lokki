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


def compressIndices(session, class_, **filter):
    """
    Compressses any gaps in indices. Does not commit the session.
    """
    objects = session.query(class_).filter_by(**filter).order_by(class_.index)
    index = 1
    for o in objects:
        print("Compressing row " + o.title + " to index " + str(index))
        o.index = index
        index += 1

