"""
Commands for managing simple invoice rows.
"""

from lokki.db.simplerow import SimpleRow
from lokki.invoice import findInvoice
from lokki.util import dieIf
from lokki.row import getNextRowIndex, findRow
from lokki.config import getSetting, isConfigurationValid

def beginRowCommand(args, session, readonly=False):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute row commands with incomplete configuration.")
  invoice = findInvoice(session, args)
  dieIf(not readonly and invoice.is_billed, 
    "Cannot execute row commands on a billed invoice.")
  return invoice

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
  row.num_units = args.num_units
  row.price_per_unit = args.price_per_unit
  session.add(row)

  session.commit()

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
