import sys
from lokki.db.client import Client

def getClientByHandle(handle, session):
  client = session.query(Client).filter_by(handle=handle).first()
  if (not client): 
    sys.stderr.write("Client not found by handle '" + handle + "'.\n");
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)
  return client

def getClientFields():
  return [
    'id',
    'handle',
    'client_number',
    'name',
    'address',
    'zip_code',
    'city',
    'country',
  ]

def getClientFieldTitle(key):
  return {
    'id'            : 'Id',
    'handle'        : 'Handle',
    'client_number' : 'Client number',
    'name'          : 'Name',
    'address'       : 'Street address',
    'zip_code'      : 'ZIP code',
    'city'          : 'City',
    'country'       : 'Country',
  }[key]
