"""
Commands to manipulate composite rows.
"""

from lokki.index import compressIndices
from lokki.db.compositerow import CompositeRow
from lokki.db.subrow import Subrow
from lokki.db.row import Row
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

  if args.external_source and args.external_id:
    query = (session.query(Row)
             .filter_by(external_source=args.external_source)
             .filter_by(external_id=args.external_id))
    dieIf(query.first(), 'External id already exists.')
  
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

def commandCompositeMerge(args, session):
    invoice = beginRowCommand(args, session)
    sourceRow = invoice.rows[int(args.source_index) - 1] 
    targetRow = invoice.rows[int(args.target_index) - 1] 
    dieIf(not isinstance(sourceRow, CompositeRow), 
          "Source row is not a composite row.");
    dieIf(not isinstance(targetRow, CompositeRow), 
          "Target row is not a composite row.");
    dieIf(sourceRow == targetRow, 
          "Source and target rows cannot be the same row.")

    subrows = sourceRow.subrows[:]
    for subrow in subrows:
        subrow.row = targetRow

    session.delete(sourceRow);

    session.commit();

    compressIndices(session, Subrow, row_id=targetRow.id)
    compressIndices(session, Row, invoice_id=invoice.id)

    session.commit();



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

