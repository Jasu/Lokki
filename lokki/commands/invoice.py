from datetime import datetime, timedelta

from lokki.db.invoice import Invoice
from lokki.db.client import Client
from lokki.invoice import *
from lokki.config import getSetting

def commandInvoiceAdd(args, session):
  checkConfiguration(session)

  invoice = Invoice()

  if args.client_handle:
    client = getClientByHandle(args.client_handle, session)
  else:
    clientId = getSetting(session, 'default-client')
    if not clientId:
      sys.stderr.write("Default client is not set and no --client-handle was set.\n")
      sys.stderr.write("Nothing done.\n")
      sys.exit(1)

    client = session.query(Client).filter_by(id=clientId).first()

  if not client:
    sys.stderr.write("Client was not found.\n")
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)

  initializeClientFields(client, invoice)

  initializeSellerFields(session, invoice)

  # Date 
  if args.date:
    date = parseDate(args.date)
  else:
    date = datetime.now()

  invoice.date = date#.strftime('%Y-%m-%d')

  if args.duedate:
    duedate = parseDate(args.duedate)
  elif args.duedays:
    duedate = date + timedelta(days=int(args.duedays))
  else:
    duedays = getSetting(session, 'default-due-days')
    if not duedays:
      sys.stderr.write("Due date not specified and no default-due-days.\n")
      sys.stderr.write("Nothing done.\n")
      sys.exit(1)
    duedate = date + timedelta(days=int(duedays))

  invoice.due_date = duedate#.strftime('%Y-%m-%d')

  # Invoice number
  if args.invoice_number:
    invoice.invoice_number = args.invoice_number
  else:
    invoice.invoice_number = getNextInvoiceNumberAndIncrement(session)

  # Reference
  invoice.reference = getReference(invoice.invoice_number, invoice.client_number)

  invoice.time_added = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')

  session.add(invoice)
  session.commit()

  print("Invoice created with number " + str(invoice.invoice_number) + ".")

def commandInvoiceRemove(args, session):
  checkConfiguration(session)

def commandInvoiceSet(args, session):
  checkConfiguration(session)

def commandInvoiceGet(args, session):
  checkConfiguration(session)

def commandInvoiceShow(args, session):
  checkConfiguration(session)

def commandInvoiceList(args, session):
  checkConfiguration(session)

def commandInvoiceBill(args, session):
  checkConfiguration(session)

def commandInvoiceUnbill(args, session):
  checkConfiguration(session)
