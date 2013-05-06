from lokki.db.subrow import Subrow
from lokki.db.compositerow import CompositeRow
from lokki.invoice import findInvoice
from lokki.util import dieIf
from lokki.row import getNextRowIndex, findRow, beginRowCommand
from lokki.compositerow import findSubrow

def commandSubrowAdd(args, session):
  invoice = beginRowCommand(args, session)
  subrow = Subrow()
  subrow.row = findRow(args, invoice, session, type=CompositeRow)
  # Note: Indexing starts from one here. Setting subrow.row in the previous
  # statement causes its insertion in subrow.row.subrows.
  subrow.index = len(subrow.row.subrows) 
  subrow.title = args.title
  subrow.num_units = args.num_units
  subrow.price_per_unit = args.price_per_unit
  if args.note:
    subrow.note = args.note
  if args.external_source:
    subrow.external_source = args.external_source
  if args.external_id:
    subrow.external_id = args.external_id

  session.add(subrow)
  session.commit()

  print("Added subrow '" + str(subrow.index) + "'.")

def commandSubrowRemove(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session, CompositeRow)
  subrow = findSubrow(args, row)

  session.delete(subrow)
  session.commit()

  print("Deleted subrow '" + str(subrow.index) + "'.")

def commandSubrowGet(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session, CompositeRow)
  subrow = findSubrow(args, row)
  dieIf(not hasattr(subrow, args.setting_name), 
    "Setting '" + args.setting_name + "' not found.")
  print(getattr(subrow, args.setting_name))

def commandSubrowSet(args, session):
  invoice = beginRowCommand(args, session)
  row = findRow(args, invoice, session, CompositeRow)
  subrow = findSubrow(args, row)
  dieIf(not hasattr(subrow, args.setting_name), 
    "Setting '" + args.setting_name + "' not found.")
  setattr(subrow, args.setting_name, args.setting_value)
  session.commit()

  print('Updated subrow ' + subrow.index 
    + ' of row ' + row.index 
    + ' of invoice ' + invoice.invoice_number + '.')

