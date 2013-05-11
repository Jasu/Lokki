import sys
from lokki.util import dieIf
from lokki.db.client import Client

def getClientByHandle(handle, session):
  client = session.query(Client).filter_by(handle=handle).first()
  dieIf(not client, "Client not found by handle '" + handle + "'.")
  return client

def getClientFields():
  return [
    'id',
    'handle',
    'client_number',
    'name',
    'address',
    'address_2',
    'zip_code',
    'city',
    'country',
    'company_number',
    'vat_number',
  ]

def getClientFieldTitle(key):
  return {
    'id' : 'Id',
    'handle' : 'Handle',
    'client_number' : 'Client number',
    'name' : 'Name',
    'address' : 'Street address',
    'address_2' : 'Street address, cont.',
    'zip_code' : 'ZIP code',
    'city' : 'City',
    'country' : 'Country',
    'company_number': 'Local company number',
    'vat_number': 'European VAT number',
  }[key]
