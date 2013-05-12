from datetime import datetime, timedelta
from decimal import Decimal
import os

from prettytable import PrettyTable
import pystache

from lokki.util import dieIf, formatNumber
from lokki.db.invoice import Invoice
from lokki.db.client import Client
from lokki.db.compositerow import CompositeRow
from lokki.invoice import *
from lokki.config import getSetting, isConfigurationValid
from lokki.event import triggerEvent

def commandInvoiceAdd(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")

  invoice = Invoice()

  if args.client_handle:
    client = getClientByHandle(args.client_handle, session)
  else:
    clientId = getSetting(session, 'default-client')
    dieIf(not clientId,
      "Default client is not set and no --client-handle was set.")
    client = session.query(Client).filter_by(id=clientId).first()

  dieIf(not client, "Default client not set and no --client-handle was set.")

  initializeClientFields(client, invoice)

  initializeSellerFields(session, invoice)

  # Date 
  if args.date:
    date = parseDate(args.date)
  else:
    date = datetime.now()

  invoice.date = date

  if args.duedate:
    duedate = parseDate(args.duedate)
  elif args.duedays:
    duedate = date + timedelta(days=int(args.duedays))
  else:
    duedays = getSetting(session, 'default-due-days')
    dieIf(not duedays, "Due date not specified and no default-due-days.")
    duedate = date + timedelta(days=int(duedays))

  invoice.due_date = duedate

  # Invoice number
  if args.invoice_number:
    invoice.invoice_number = args.invoice_number
  else:
    invoice.invoice_number = getNextInvoiceNumberAndIncrement(session)

  # Reference
  invoice.reference = getReference(invoice.invoice_number, invoice.client_number)

  invoice.time_added = datetime.now()

  session.add(invoice)
  session.commit()

  print("Invoice created with number " + str(invoice.invoice_number) + ".")

def commandInvoiceRemove(args, session):
  invoice = session.query(Invoice).filter_by(invoice_number=args.invoice_number).first()
  dieIf(not invoice, "Invoice not found by number '"+args.invoice_number+"'.")
  dieIf(invoice.is_billed, "Cannot remove a billed invoice.")

  session.delete(invoice)
  session.commit()

def commandInvoiceSet(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")

  invoice = findInvoice(session, args)

  dieIf(not hasattr(invoice, args.setting_name), 
    "Invoice setting '" + args.setting_name + "' does not exist.")

  setattr(invoice, args.setting_name, args.setting_value)
  session.commit()

def commandInvoiceGet(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")

  invoice = findInvoice(session, args)

  dieIf(not hasattr(invoice, args.setting_name), 
    "Invoice setting '" + args.setting_name + "' does not exist.")

  print(getattr(invoice, args.setting_name))

def commandInvoiceShow(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")

  invoice = findInvoice(session, args)

  table = PrettyTable(['Seller info', ''])
  table.align['Seller info'] = 'r'
  table.align[''] = 'l'

  table.add_row(['Name', invoice.seller_name])
  table.add_row(['Address', invoice.seller_address])
  table.add_row(['ZIP code', invoice.seller_zip_code])
  table.add_row(['City', invoice.seller_city])
  if invoice.seller_country:
    table.add_row(['Country', invoice.seller_country])

  print(table)
  print('')

  table = PrettyTable(['Client info', ''])
  table.align['Client info'] = 'r'
  table.align[''] = 'l'

  table.add_row(['Name', invoice.client_name])
  table.add_row(['Client number', invoice.client_number])
  table.add_row(['Address', invoice.client_address])
  table.add_row(['ZIP code', invoice.client_zip_code])
  table.add_row(['City', invoice.client_city])
  if invoice.client_country:
    table.add_row(['Country', invoice.client_country])

  print(table)
  print('')

  table = PrettyTable(['Invoice', ''])
  table.align['Invoice'] = 'r'
  table.align[''] = 'l'

  table.add_row(['Created', invoice.time_added.strftime('%Y-%m-%d %H:%M:%S')])
  table.add_row(['Date', invoice.date.strftime('%Y-%m-%d')])
  table.add_row(['Due date', invoice.due_date.strftime('%Y-%m-%d')])
  table.add_row(['IBAN', invoice.seller_iban])
  table.add_row(['Invoice number', invoice.invoice_number])
  table.add_row(['Reference', invoice.reference])
  table.add_row(['Is billed', 'Yes' if invoice.is_billed else 'Not billed'])

  print(table)

  table = PrettyTable(['N', 'Item', 'Units', 'Price/unit', 'Total', '*'])
  table.align['N'] = 'l'
  table.align['Item'] = 'l'
  table.align['Units'] = 'l'
  table.align['Price/unit'] = 'l'
  table.align['Total'] = 'l'
  table.align['*'] = 'l'

  for row in invoice.rows:
    extra = []
    if row.note:
      extra.append('note')
    if isinstance(row, CompositeRow):
      extra.append('composite')
    table.add_row([
      row.index,
      row.title,
      row.getNumberOfUnits(),
      row.getPricePerUnit(),
      row.getTotal(),
      ', '.join(extra)
    ])

  print('')
  print(table)

def commandInvoiceList(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")
  invoices = session.query(Invoice)
  table = PrettyTable(['Number', 'Date', 'Reference', 'Client', 'Sum'])
  table.padding_width = 1

  for invoice in invoices:
    table.add_row([
      invoice.invoice_number,
      invoice.date,
      invoice.reference,
      invoice.client.name,
      'TODO',
    ])

  print(table)

def commandInvoiceBill(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")

  invoice = findInvoice(session, args)

  dieIf(invoice.is_billed, 
    "Invoice " + str(invoice.invoice_number) + " was already billed.")

  invoice.is_billed = True
  session.commit()

  print ("Marked invoice '" + str(invoice.invoice_number) + "' as billed.")

def commandInvoiceUnbill(args, session):
  dieIf(not isConfigurationValid(session), 
    "Cannot execute invoicing commands with incomplete configuration.")

  invoice = findInvoice(session, args)

  dieIf(not invoice.is_billed, 
    "Invoice " + str(invoice.invoice_number) + " was not billed.")

  invoice.is_billed = False
  session.commit()

  print ("Marked invoice '" + str(invoice.invoice_number) + "' as not billed.")

def commandInvoiceGenerate(args, session):
  if args.template:
    template = args.template
  else:
    template = getSetting(session, 'default-invoice-template')

  dieIf(not template, 
        'No --template provided and default-invoice-template not set.')

  invoice = findInvoice(session, args)

  with open(template, 'r') as template:
    templateString = template.read()

  rows = []
  composite_rows = []

  total = Decimal(0)
  total_vat = Decimal(0)
  for row in invoice.rows:
    rowData = {
      'title': row.title,
      'num_units': formatNumber(row.getNumberOfUnits()),
      'vat': formatNumber(row.vat),
      'vat_percentage': formatNumber(Decimal(row.vat) * 100),
      'total': formatNumber(Decimal(row.getTotal())),
      'total_with_vat': formatNumber(row.getTotal() * (1 + Decimal(row.vat))),
    }
    if row.getPricePerUnit(): 
      rowData['price_per_unit'] = formatNumber(row.getPricePerUnit()),
    if isinstance(row, CompositeRow):
      rowData['subrows'] = []
      for subrow in row.subrows:
        row_total = Decimal(subrow.num_units) * Decimal(subrow.price_per_unit)
        rowData['subrows'].append({
          'title': subrow.title,
          'price_per_unit': formatNumber(subrow.price_per_unit),
          'num_units': formatNumber(subrow.num_units),
          'vat': formatNumber(row.vat),
          'vat_percentage': formatNumber(Decimal(row.vat) * 100),
          'total': formatNumber(row_total),
          'total_with_vat': formatNumber(row_total * (1 + Decimal(row.vat))),
        })
      composite_rows.append(rowData)

    rows.append(rowData)

    total += row.getTotal()
    total_vat += row.getTotal() * Decimal(row.vat)

  templateArguments = {
    'show_details': not args.hide_details and len(composite_rows),
    'rows': rows,
    'composite_rows': composite_rows, 
    'invoice': invoice,
    'n': '%05d' % invoice.invoice_number,
    'd': '%02d' % datetime.today().day,
    'm': '%02d' % datetime.today().month,
    'y': '%04d' % datetime.today().year,
    'due_days': (invoice.due_date - invoice.date).days,
    'total': formatNumber(total),
    'total_vat': formatNumber(total_vat),
    'total_with_vat': formatNumber(total + total_vat),
    'currency':'€',
  }

  renderedInvoice = pystache.render(templateString, templateArguments)

  if args.filename: 
    targetPath = args.filename
  else:
    targetFilenameTemplate = getSetting(session, 'invoice-filename-template')
    targetPath = pystache.render(targetFilenameTemplate, templateArguments)

  targetPath = os.path.normpath(targetPath)

  templateArguments['output_path'] = targetPath
  templateArguments['output_basename'] = os.path.basename(targetPath)
  (templateArguments['output_path_no_ext'], 
   templateArguments['output_path_ext']) = os.path.splitext(targetPath)

  with open(targetPath, 'w') as output:
    output.write(renderedInvoice)

  triggerEvent(session, 'generate', templateArguments)

