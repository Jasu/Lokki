from lokki.db.subrow import Subrow
from lokki.db.compositerow import CompositeRow
from lokki.util import dieIf
from lokki.row import getNextRowIndex, findRow, beginRowCommand
from lokki.compositerow import findSubrow
from lokki.index import compressIndices

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
    if args.external_source and args.external_id:
        query = (session.query(Subrow)
                 .filter_by(external_source=args.external_source)
                 .filter_by(external_id=args.external_id))
        dieIf(query.first(), 'External id already exists.')

    session.add(subrow)
    session.commit()

    print("Added subrow '" + str(subrow.index) + "'.")

def commandSubrowRemove(args, session):
    invoice = beginRowCommand(args, session)
    row = findRow(args, invoice, session, CompositeRow)
    subrow = findSubrow(row, args.subrow_index)
  
    session.delete(subrow)
    session.commit()
  
    print("Deleted subrow '" + str(subrow.index) + "'.")

def commandSubrowGet(args, session):
    invoice = beginRowCommand(args, session)
    row = findRow(args, invoice, session, CompositeRow)
    subrow = findSubrow(row, args.subrow_index)
    dieIf(not hasattr(subrow, args.setting_name), 
          "Setting '" + args.setting_name + "' not found.")
    print(getattr(subrow, args.setting_name))

def commandSubrowSet(args, session):
    invoice = beginRowCommand(args, session)
    row = findRow(args, invoice, session, CompositeRow)
    subrow = findSubrow(row, args.subrow_index)
    dieIf(not hasattr(subrow, args.setting_name), 
          "Setting '" + args.setting_name + "' not found.")
    setattr(subrow, args.setting_name, args.setting_value)
    session.commit()
  
    print('Updated subrow ' + subrow.index 
          + ' of row ' + row.index 
          + ' of invoice ' + invoice.invoice_number + '.')

def commandSubrowMv(args, session):
    invoice = beginRowCommand(args, session)
    srcRow = invoice.rows[int(args.src_row_index) - 1]
    dstRow = invoice.rows[int(args.dst_row_index) - 1]

    if srcRow == dstRow:
        print('Source and destination are the same row.')
        print('Nothing done.')
        return 

    subrow = findSubrow(srcRow, args.subrow_index)

    subrow.row_id = dstRow.id
    subrow.index = len(dstRow.subrows) + 1
    session.commit()

    compressIndices(session, Subrow, row_id=srcRow.id)

    session.commit()

