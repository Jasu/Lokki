from pprint import pprint
from lokki.util import dieIf
from lokki.db.simplerow import SimpleRow
import sys

def getNextRowIndex(invoice):
  return len(invoice.rows) + 1

def findRow(args, invoice, session):
  if args.index:
    dieIf(int(args.index) > len(invoice.rows), 'Row index is too large.')
    dieIf(int(args.index) < 1, 'Row index below one.')
    row = invoice.rows[int(args.index) - 1]
  else:
    row = invoice.rows[-1]
  dieIf(not isinstance(row, SimpleRow), 'Selected row is not a simple row.')
  return row
  
