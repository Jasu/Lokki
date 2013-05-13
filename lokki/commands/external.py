import json

from prettytable import PrettyTable

from lokki.db.row import Row
from lokki.db.subrow import Subrow

def commandExternalRows(args, session):
  _command(args, session, Row)

def commandExternalSubrows(args, session):
  _command(args, session, Subrow)


def _command(args, session, class_):
  query = (session.query(class_)
                  .filter(class_.external_id != None)
                  .filter(class_.external_source == args.external_source))

  result = {}
  for row in query:
    result[row.external_id] = row.id

  if args.json:
    print(json.dumps(result))
  else:
    table = PrettyTable(['External ID', 'Row ID'])
    for external_id, row_id in result.items():
      table.add_row([external_id, row_id])
    print(table)
