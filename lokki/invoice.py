import sys
from lokki.db.setting import Setting
from lokki.config import isConfigurationValid, getConfiguration
from lokki.client import getClientByHandle

def checkConfiguration(session):
  if not isConfigurationValid(session):
    sys.stderr.write("Configuration must be complete before invoicing.\n")
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)

def getNextInvoiceNumberAndIncrement(session):
  """
  Does not commit the session, to allow transaction semantics.
  """
  setting = session.query(Setting).filter_by(name='next-invoice-number').first()
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
    checksum += remainder % 10
    remainder = int(remainder / 10)

    if weight == 7:
      weight = 3
    elif weight == 3:
      weight = 1
    else:
      weight = 7
  checksum = 10 - checksum % 10
  return str(reference) + str(checksum)


def getReference(invoiceNumber, clientNumber):
  reference = int(clientNumber) * 1000000 + int(invoiceNumber)
  return addChecksum(reference)

def initializeClientFields(client, invoice):
  """
  Fills in client_id and copies client data to the invoice.
  """

  invoice.client_name = client.name
  if client.client_number:
    invoice.client_number = client.client_number
  else:
    invoice.client_number = client.id
  invoice.client_address = client.address
  invoice.client_zip_code = client.zip_code
  invoice.client_city = client.city
  invoice.client_country = client.country

def initializeSellerFields(session, invoice):
  """
  Fills in seller_* fields in the invoice from configuration
  """
  configuration = getConfiguration(session)

  invoice.seller_name = configuration['seller-name']
  invoice.seller_address = configuration['seller-address']
  invoice.seller_zip_code = configuration['seller-zip-code']
  invoice.seller_city = configuration['seller-city']
  invoice.seller_country = configuration['seller-country']
  invoice.seller_iban = configuration['seller-iban']

def parseDate(date):
  if '.' in date:
    # Finnish date
    return datetime.strptime(date, '%d.%m.%Y')
  else:
    # ISO date
    return datetime.strptime(date, '%Y-%m-%d')

