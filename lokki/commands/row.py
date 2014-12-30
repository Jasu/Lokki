"""
Commands for managing simple invoice rows.
"""

from lokki.db.simplerow import SimpleRow
from lokki.db.row import Row
from lokki.db.invoice import Invoice
from lokki.invoice import findInvoice
from lokki.util import dieIf
from lokki.row import getNextRowIndex, findRow, beginRowCommand, jsonPrintRow
from lokki.config import getSetting, isConfigurationValid
from lokki.index import compressIndices

def commandRowAdd(args, session):
  invoice = beginRowCommand(args, session)
  row = SimpleRow()
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

  row.num_units = args.num_units
  row.price_per_unit = args.price_per_unit
  session.add(row)

  session.commit()

  if args.json:
    jsonPrintRow(row)
  else:
    print("Added row '" + str(row.index) + "'.")

def commandRowRemove(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session)

  session.delete(row)

  session.commit()

  print("Deleted row '" + str(row.index) + "'.")

def commandRowSet(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session)
  dieIf(not hasattr(row, args.setting_name), 
    "Setting '" + args.setting_name + "' does not exist.")

  setattr(row, args.setting_name, args.setting_value)

  session.commit()

  print("Updated row '" + str(row.index) + "'.")

def commandRowGet(args, session):
  invoice = beginRowCommand(args, session, readonly=True)
  row = findRow(args, invoice, session)
  dieIf(not hasattr(row, args.setting_name), 
    "Setting '" + args.setting_name + "' does not exist.")
  print(getattr(row, args.setting_name))

def commandRowMv(args, session):
    dieIf(not isConfigurationValid(session), 
        "Cannot execute row commands with incomplete configuration.")
    src_invoice = (session.query(Invoice)
        .filter_by(invoice_number=args.src_invoice_number)
        .first())
    dst_invoice = (session.query(Invoice)
        .filter_by(invoice_number=args.dst_invoice_number)
        .first())
    dieIf(src_invoice.is_billed, 
        "Cannot execute row commands on a billed source invoice.")
    dieIf(dst_invoice.is_billed, 
        "Cannot execute row commands on a billed source invoice.")
    dieIf(int(args.row) > len(src_invoice.rows), 'Row index is too large.')
    dieIf(int(args.row) < 1, 'Row index below one.')
    row = src_invoice.rows[int(args.row) - 1]
    row.invoice = dst_invoice

    session.commit()
    compressIndices(session, Row, invoice=dst_invoice)
    compressIndices(session, Row, invoice=src_invoice)
    session.commit()
    print("Moved row '" + str(row.index) + "'.")
