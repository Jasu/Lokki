"""
Commands to manipulate composite rows.
"""

from lokki.db.compositerow import CompositeRow
from lokki.db.subrow import Subrow
from lokki.invoice import findInvoice
from lokki.util import dieIf
from lokki.row import getNextRowIndex, findRow, beginRowCommand, jsonPrintRow
from lokki.compositerow import findSubrow
from lokki.config import getSetting
from prettytable import PrettyTable
from decimal import Decimal

def commandCompositeAdd(args, session):
  invoice = beginRowCommand(args, session)
  row = CompositeRow()
  row.index = getNextRowIndex(invoice)
  row.invoice = invoice
  row.title = args.title
  if args.vat:
    row.vat = args.vat
  else:
    row.vat = getSetting(session, 'default-vat')
    dieIf(not row.vat, "default-vat is not set and no VAT was provided.")
  if args.note:
    row.note = args.note
  if args.external_source:
    row.external_source = args.external_source
  if args.external_id:
    row.external_id = args.external_id
  
  session.add(row)
  session.commit()

  if args.json:
    jsonPrintRow(row)
  else:
    print("Added row '" + str(row.index) + "'.")

def commandCompositeRemove(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session, CompositeRow)

  session.delete(row)

  session.commit()

  print("Deleted row '" + str(row.index) + "'.")

def commandCompositeShow(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session, CompositeRow)
  table = PrettyTable(['N', 'Title', 'Price per unit', 'Num units', 'Total'])

  for subrow in row.subrows:
    table.add_row([
      subrow.index,
      subrow.title,
      subrow.price_per_unit,
      subrow.num_units,
      Decimal(subrow.price_per_unit) * Decimal(subrow.num_units),
    ])

  print(table)

