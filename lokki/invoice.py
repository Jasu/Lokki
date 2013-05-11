import sys
from lokki.db.setting import Setting
from lokki.db.invoice import Invoice
from lokki.config import isConfigurationValid, getConfiguration
from lokki.client import getClientByHandle
from lokki.util import dieIf

def getNextInvoiceNumberAndIncrement(session):
  """
  Does not commit the session, to allow transaction semantics.
  """
  setting = session.query(Setting).filter_by(name='next-invoice-number').first()
  dieIf(not setting, "Next invoice number is not set.")
  result = setting.value
  setting.value = int(setting.value) + 1
  return result

def addChecksum(reference):
  """
  Given a Finnish reference code without the checksum digit, appends the 
  checksum digit to it.
  """
  checksum = 0
  remainder = reference
  weight = 7
  while remainder:
    checksum += weight * (remainder % 10)
    remainder = int(remainder / 10)

    if weight == 7:
      weight = 3
    elif weight == 3:
      weight = 1
    else:
      weight = 7

  checksum = 10 - checksum % 10
  if checksum == 10:
    checksum = 0
  return str(reference) + str(checksum)


def getReference(invoiceNumber, clientNumber):
  reference = int(clientNumber) * 1000000 + int(invoiceNumber)
  return addChecksum(reference)

def initializeClientFields(client, invoice):
  """
  Fills in client_id and copies client data to the invoice.
  """

  invoice.client = client

  invoice.client_name = client.name
  if client.client_number:
    invoice.client_number = client.client_number
  else:
    invoice.client_number = client.id
  invoice.client_address = client.address
  invoice.client_address_2 = client.address_2
  invoice.client_zip_code = client.zip_code
  invoice.client_city = client.city
  invoice.client_country = client.country
  invoice.client_company_number = client.company_number
  invoice.client_vat_number = client.vat_number

def initializeSellerFields(session, invoice):
  """
  Fills in seller_* fields in the invoice from configuration
  """
  configuration = getConfiguration(session)

  invoice.seller_name = configuration['seller-name']
  invoice.seller_address = configuration['seller-address']
  if 'seller-adddress-2' in configuration:
    invoice.seller_address_2 = configuration['seller-address-2']
  invoice.seller_zip_code = configuration['seller-zip-code']
  invoice.seller_city = configuration['seller-city']
  if 'seller-country' in configuration:
    invoice.seller_country = configuration['seller-country']
  invoice.seller_iban = configuration['seller-iban']
  invoice.seller_company_number = configuration['seller-company-number']
  if 'seller-vat-number' in configuration:
    invoice.seller_vat_number = configuration['seller-vat-number']


def parseDate(date):
  if '.' in date:
    # Finnish date
    return datetime.strptime(date, '%d.%m.%Y')
  else:
    # ISO date
    return datetime.strptime(date, '%Y-%m-%d')

def findInvoice(session, args):
  if args.invoice_number:
    invoice = session.query(Invoice).filter_by(invoice_number=args.invoice_number).first()
    dieIf(not invoice, 
      "Invoice not found by invoice number '" + args.invoice_number+"'.")
    return invoice
  else:
    invoice = (session.query(Invoice)
                      .order_by(Invoice.time_added.desc())
                      .first())
    dieIf(not invoice, "No invoices exist yet.")
    return invoice

