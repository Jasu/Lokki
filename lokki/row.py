from pprint import pprint
from lokki.util import dieIf
from lokki.invoice import findInvoice
from lokki.config import isConfigurationValid
from lokki.db.simplerow import SimpleRow
import sys

def getNextRowIndex(invoice):
  return len(invoice.rows) + 1

def findRow(args, invoice, session, type=SimpleRow):
  index = None
  if 'index' in args and args.index:
    index = args.index
  elif 'row_index' in args and args.row_index:
    index = args.row_index
  if index:
    dieIf(int(args.index) > len(invoice.rows), 'Row index is too large.')
    dieIf(int(args.index) < 1, 'Row index below one.')
    row = invoice.rows[int(args.index) - 1]
  else:
    row = invoice.rows[-1]
  dieIf(not isinstance(row, type), 'Selected row is not a simple row.')
  return row
  
def beginRowCommand(args, session, readonly=False):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute row commands with incomplete configuration.")
  invoice = findInvoice(session, args)
  dieIf(not readonly and invoice.is_billed, 
    "Cannot execute row commands on a billed invoice.")
  return invoice

