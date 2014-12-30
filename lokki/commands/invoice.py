from datetime import datetime, timedelta
from decimal import Decimal
import os
import json
from pprint import pprint

from prettytable import PrettyTable
import pystache

from lokki.index import compressIndices
from lokki.util import dieIf, formatNumber
from lokki.db.invoice import Invoice
from lokki.db.client import Client
from lokki.db.row import Row
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
    invoice.reference = getReference(invoice.invoice_number,
                                     invoice.client_number)

    invoice.time_added = datetime.now()

    session.add(invoice)
    session.commit()

    if args.json:
        _jsonPrintInvoice(invoice)
    else:
        print("Invoice created with number "
              + str(invoice.invoice_number) + ".")


def commandInvoiceRemove(args, session):
    invoice = (session.query(Invoice)
                      .filter_by(invoice_number=args.invoice_number)
                      .first())
    dieIf(not invoice,
          "Invoice not found by number '"+args.invoice_number+"'.")
    dieIf(invoice.is_billed, "Cannot remove a billed invoice.")

    session.delete(invoice)
    session.commit()


def commandInvoiceSet(args, session):
    dieIf(not isConfigurationValid(session),
          "Cannot execute invoicing commands with incomplete configuration.")

    invoice = findInvoice(session, args)

    dieIf(not hasattr(invoice, args.setting_name),
          "Invoice setting '" + args.setting_name + "' does not exist.")

    if args.setting_name in ['date', 'due_date']:
        value = parseDate(args.setting_value)
    else:
        value = args.setting_value

    setattr(invoice, args.setting_name, value)
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

    if args.json:
        _jsonPrintInvoice(invoice)
    else:
        table = PrettyTable(['Seller info', ''])
        table.align['Seller info'] = 'r'
        table.align[''] = 'l'

        table.add_row(['Name', invoice.seller_name])
        table.add_row(['Address', invoice.seller_address])
        table.add_row(['ZIP code', invoice.seller_zip_code])
        table.add_row(['City', invoice.seller_city])
        if invoice.seller_country:
            table.add_row(['Country', invoice.seller_country])
        if invoice.seller_company_number:
            table.add_row(['Company number', invoice.seller_company_number])
        if invoice.seller_vat_number:
            table.add_row(['VAT number', invoice.seller_vat_number])

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
        if invoice.client_company_number:
            table.add_row(['Company number', invoice.client_company_number])
        if invoice.client_vat_number:
            table.add_row(['VAT number', invoice.client_vat_number])

        print(table)
        print('')

        table = PrettyTable(['Invoice', ''])
        table.align['Invoice'] = 'r'
        table.align[''] = 'l'

        table.add_row(['Created',
                       invoice.time_added.strftime('%Y-%m-%d %H:%M:%S')])
        table.add_row(['Date', invoice.date.strftime('%Y-%m-%d')])
        table.add_row(['Due date', invoice.due_date.strftime('%Y-%m-%d')])
        table.add_row(['IBAN', invoice.seller_iban])
        table.add_row(['Invoice number', invoice.invoice_number])
        table.add_row(['Reference', invoice.reference])
        table.add_row(['Is billed',
                       'Yes' if invoice.is_billed else 'Not billed'])

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
            if row.external_source != 'lk': 
                extra.append(row.external_source)
            table.add_row([
                row.index,
                row.title,
                formatNumber(row.getNumberOfUnits()),
                formatNumber(row.getPricePerUnit()),
                formatNumber(row.getTotal()),
                ', '.join(extra)
            ])

        print('')
        print(table)

        print('')
        print('Total without VAT:   ' + formatNumber(invoice.getTotal()))
        print('Total VAT:           ' + formatNumber(invoice.getTotalVAT()))
        print('Total with VAT       ' + formatNumber(invoice.getTotalWithVAT()))


def commandInvoiceList(args, session):
    dieIf(not isConfigurationValid(session),
          "Cannot execute invoicing commands with incomplete configuration.")
    invoices = session.query(Invoice)
    table = PrettyTable(['Number', 'Date', 'Reference', 'Client', 'Sum', 'Status'])
    table.padding_width = 1

    for invoice in invoices:
        table.add_row([
            invoice.invoice_number,
            invoice.date,
            invoice.reference,
            invoice.client.name,
            invoice.getTotal(),
            "Billed" if invoice.is_billed else "Not billed",
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

    triggerEvent(session, 'bill', _getTemplateArguments(invoice))

    print("Marked invoice '" + str(invoice.invoice_number) + "' as billed.")


def commandInvoiceUnbill(args, session):
    dieIf(not isConfigurationValid(session),
          "Cannot execute invoicing commands with incomplete configuration.")

    invoice = findInvoice(session, args)

    dieIf(not invoice.is_billed,
          "Invoice " + str(invoice.invoice_number) + " was not billed.")

    invoice.is_billed = False
    session.commit()

    triggerEvent(session, 'unbill', _getTemplateArguments(invoice))

    print("Marked invoice '"
          + str(invoice.invoice_number) + "' as not billed.")


def commandInvoiceMerge(args, session):
    sourceInvoice = (session.query(Invoice)
                    .filter_by(invoice_number=args.source_invoice_number)
                    .first())

    targetInvoice = (session.query(Invoice)
                    .filter_by(invoice_number=args.target_invoice_number)
                    .first())

    dieIf(not sourceInvoice, "Source invoice not found.")
    dieIf(not targetInvoice, "Target invoice not found.")
    dieIf(sourceInvoice.is_billed, "Source invoice is billed.")
    dieIf(targetInvoice.is_billed, "Target invoice is billed.")

    #Make copy of the array, since elements are removed from it during moving,
    #making for loop to iterate only 1/2 rows.
    rows = sourceInvoice.rows[:]
    for row in rows:
        print ("Moving row #" + str(row.id) + ".")
        row.invoice = targetInvoice

    session.commit()

    compressIndices(session, Row, invoice_id=targetInvoice.id)

    session.commit()

    print("Moved rows from invoice #" + str(args.source_invoice_number)
            + " to invoice #" + str(args.target_invoice_number) + ".")


def _getTemplateArguments(invoice):
    rows = []
    composite_rows = []
    simple_rows = []

    total = Decimal(0)
    total_vat = Decimal(0)
    for row in invoice.rows:
        rowData = {
            'title': row.title,
            'num_units': formatNumber(row.getNumberOfUnits()),
            'vat': formatNumber(row.vat),
            'vat_percentage': formatNumber(Decimal(row.vat) * 100),
            'total': formatNumber(Decimal(row.getTotal())),
            'total_vat': formatNumber(row.getTotal() * Decimal(row.vat)),
            'total_with_vat':
            formatNumber(row.getTotal() * (1 + Decimal(row.vat))),
        }
        if row.getPricePerUnit():
            rowData['price_per_unit'] = formatNumber(row.getPricePerUnit())
        if isinstance(row, CompositeRow):
            rowData['subrows'] = []
            for subrow in row.subrows:
                row_total = (Decimal(subrow.num_units)
                             * Decimal(subrow.price_per_unit))
                rowData['subrows'].append({
                    'title': subrow.title,
                    'price_per_unit': formatNumber(subrow.price_per_unit),
                    'num_units': formatNumber(subrow.num_units),
                    'vat': formatNumber(row.vat),
                    'vat_percentage': formatNumber(Decimal(row.vat) * 100),
                    'total': formatNumber(row_total),
                    'total_with_vat':
                    formatNumber(row_total * (1 + Decimal(row.vat))),
                })
            composite_rows.append(rowData)
        else:
            simple_rows.append(rowData)

        rows.append(rowData)

        total += row.getTotal()
        total_vat += row.getTotal() * Decimal(row.vat)

    lokki_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    return {
        'rows': rows,
        'has_simple_rows': len(simple_rows) > 0,
        'simple_rows': simple_rows,
        'has_composite_rows': len(composite_rows) > 0,
        'composite_rows': composite_rows,
        'invoice': invoice,
        'n': '%05d' % invoice.invoice_number,
        'd': '%02d' % datetime.today().day,
        'm': '%02d' % datetime.today().month,
        'y': '%04d' % datetime.today().year,

        'invoice_d': '%02d' % invoice.date.day,
        'invoice_m': '%02d' % invoice.date.month,
        'invoice_y': '%04d' % invoice.date.year,

        'due_d': '%02d' % invoice.due_date.day,
        'due_m': '%02d' % invoice.due_date.month,
        'due_y': '%04d' % invoice.due_date.year,

        'lokki_dir': lokki_dir,

        'due_days': (invoice.due_date - invoice.date).days,
        'total': formatNumber(total),
        'total_vat': formatNumber(total_vat),
        'total_with_vat': formatNumber(total + total_vat),
        'currency': '€',
    }


def commandInvoiceGenerate(args, session):
    if args.template:
        template = args.template
    else:
        template = getSetting(session, 'default-invoice-template')
        lokki_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template = lokki_dir + '/' + template

    dieIf(not template,
          'No --template provided and default-invoice-template not set.')

    invoice = findInvoice(session, args)

    templateArguments = _getTemplateArguments(invoice)
    templateArguments['show_details'] = (not args.hide_details
            and len(templateArguments['composite_rows']))

    with open(template, 'r') as template:
        templateString = template.read()

    renderedInvoice = pystache.render(templateString, templateArguments)

    if args.filename:
        targetPath = args.filename
    else:
        targetFilenameTemplate = getSetting(session,
                                            'invoice-filename-template')
        targetPath = pystache.render(targetFilenameTemplate, templateArguments)

    targetPath = os.path.normpath(targetPath)

    templateArguments['output_path'] = targetPath
    templateArguments['output_basename'] = os.path.basename(targetPath)
    (templateArguments['output_path_no_ext'],
     templateArguments['output_path_ext']) = os.path.splitext(targetPath)

    with open(targetPath, 'w') as output:
        output.write(renderedInvoice)

    triggerEvent(session, 'generate', templateArguments)


def _jsonPrintInvoice(invoice):
    rows = []
    simple_rows = []
    composite_rows = []
    for row in invoice.rows:
        rowTable = {
            'title': row.title,
            'type:': row.type,
            'index': row.index,
            'vat': row.vat,
            'total': float(row.getTotal()),
            'price_per_unit':
            float(row.getPricePerUnit()) if row.getPricePerUnit() else None,
            'num_units':
            float(row.getNumberOfUnits()) if row.getNumberOfUnits() else None,
        }
        if isinstance(row, CompositeRow):
            rowTable['subrows'] = []
            for subrow in row.subrows:
                rowTable['subrows'].append({
                    'title': subrow.title,
                    'price_per_unit': float(subrow.price_per_unit),
                    'num_units': float(subrow.num_units),
                    'total': float(Decimal(subrow.num_units)
                                   * Decimal(subrow.price_per_unit)),
                })
            composite_rows.append(rowTable)
        else:
            simple_rows.append(rowTable)
        rows.append(rowTable)
    print(json.dumps({
        'invoice': {
          'id': invoice.id,
          'invoice_number': invoice.invoice_number,
          'time_added': invoice.time_added.isoformat(),
          'date': invoice.date.isoformat(),
          'due_date': invoice.due_date.isoformat(),
          'reference': invoice.reference,
          'is_billed': invoice.is_billed,
          'client_id': invoice.client_id,

          'seller_name': invoice.seller_name,
          'seller_address': invoice.seller_address,
          'seller_address_2': invoice.seller_address_2,
          'seller_zip_code': invoice.seller_zip_code,
          'seller_city': invoice.seller_city,
          'seller_country': invoice.seller_country,
          'seller_phone_number': invoice.seller_phone_number,
          'seller_company_number': invoice.seller_company_number,
          'seller_vat_number': invoice.seller_vat_number,
          'seller_iban': invoice.seller_iban,

          'client_name': invoice.client_name,
          'client_number': invoice.client_number,
          'client_address': invoice.client_address,
          'client_address_2': invoice.client_address_2,
          'client_zip_code': invoice.client_zip_code,
          'client_city': invoice.client_city,
          'client_country': invoice.client_country,
          'client_company_number': invoice.client_company_number,
          'client_vat_number': invoice.client_vat_number,

          'rows': rows,
          'simple_rows': simple_rows,
          'composite_rows': composite_rows,
          }
    }))
