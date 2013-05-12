
from lokki.db.eventhandler import EventHandler
from lokki.index import getNextIndex

from prettytable import PrettyTable

def _findHandler(args, session):
  query = session.query(EventHandler)
  if args.id:
    query = query.filter_by(id=args.id)
  elif args.index and args.event:
    query = query.filter_by(event=args.event, index=args.index)
  else:
    dieIf(True, 'No criteria provided.')

  handler = query.first()
  dieIf(not handler, 'Handler not found.')

  return handler

def commandEventAdd(args, session):
  handler = EventHandler()

  handler.index = getNextIndex(session, EventHandler, event=args.event)
  handler.event = args.event
  handler.command = args.command

  session.add(handler)

  session.commit()

def commandEventRemove(args, session):
  handler = _findHandler(args, session)

  session.delete(handler)
  session.commit()

def commandEventSet(args, session):
  handler = _findHandler(args, session)
  dieIf(not hasattr(handler, args.setting_name), 'Setting not found.')
  setattr(handler, args.setting_name, args.setting_value)
  session.commit()

def commandEventGet(args, session):
  handler = _findHandler(args, session)
  dieIf(not hasattr(handler, args.setting_name), 'Setting not found.')
  print(getattr(handler, args.setting_name))

def commandEventList(args, session):
  query  = (session
            .query(EventHandler)
            .order_by(EventHandler.event, EventHandler.index))

  if args.event:
    query = query.filter_by(event=args.event)
    table = PrettyTable(['Index', 'Command'])
  else:
    table = PrettyTable(['Event', 'Index', 'Command'])
    table.align['Event'] = 'r'
  table.align['Index'] = 'r'
  table.align['Command'] = 'l'
  
  for event in query:
    row = []
    if not args.event:
      row.append(event.event)
    row.append(event.index)
    row.append(event.command)
    table.add_row(row)

  print(table)

