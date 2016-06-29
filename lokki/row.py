import sys
import json
from pprint import pprint

from lokki.util import dieIf
from lokki.invoice import findInvoice
from lokki.config import isConfigurationValid
from lokki.db.simplerow import SimpleRow
from lokki.db.compositerow import CompositeRow

def getNextRowIndex(invoice):
  return len(invoice.rows) + 1

def findRow(args, invoice, session, type=SimpleRow):
  index = None
  if 'index' in args and args.index:
    index = args.index
  elif 'row' in args and args.row:
    index = args.row
  if index:
    dieIf(int(index) > len(invoice.rows), 'Row index is too large.')
    dieIf(int(index) < 1, 'Row index below one.')
    row = invoice.rows[int(index) - 1]
  else:
    row = invoice.rows[-1]
  dieIf(type and not isinstance(row, type), 'Selected row is not a simple row.')
  return row
  
def beginRowCommand(args, session, readonly=False):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute row commands with incomplete configuration.")
  invoice = findInvoice(session, args)
  dieIf(not readonly and invoice.is_billed, 
    "Cannot execute row commands on a billed invoice.")
  return invoice

def jsonPrintRow(row):
  rowTable = {
    'title': row.title,
    'index': row.index,
    'type:': row.type,
    'vat': row.vat,
    'total': float(row.getTotal()),
    'price_per_unit': float(row.getPricePerUnit()) if row.getPricePerUnit() else None,
    'num_units': float(row.getNumberOfUnits()) if row.getNumberOfUnits() else None,
  }
  if isinstance(row, CompositeRow):
    rowTable['subrows'] = []
    for subrow in row.subrows:
      rowTable['subrows'].append({
        'title': subrow.title,
        'price_per_unit': float(subrow.price_per_unit),
        'num_units': float(subrow.num_units),
        'total': float(Decimal(subrow.num_units) * Decimal(price_per_unit))
      })
  print(json.dumps(rowTable))
