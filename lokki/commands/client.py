from prettytable import PrettyTable
from lokki.db.client import Client
from lokki.client import getClientByHandle, getClientFields, getClientFieldTitle
from lokki.util import dieIf

def commandClientAdd(args, session):
  client = Client()
  client.handle = args.handle

  if 'name' in args and args.name:
    client.name = args.name
  if 'address' in args and args.address:
    client.address = args.address
  if 'zip_code' in args and args.zip_code:
    client.zip_code = args.zip_code
  if 'city' in args and args.city:
    client.city = args.city
  if 'country' in args and args.country:
    client.country = args.country
  if 'client_number' in args and args.client_number:
    clientByNumber = (session.query(Client)
                        .filter_by(client_number=args.client_number)
                        .first())
    dieIf(clientByNumber, 
      "Client already exists by client number '" + args.client_number + "'.")
    client.client_number = args.client_number

  session.add(client)
  session.commit()

  print("Client was added.")

def commandClientRemove(args, session):
  client = getClientByHandle(args.handle, session)

  session.delete(client)
  session.commit()

  print("Client '" + args.handle + "' was deleted.")

def commandClientSet(args, session):
  client = getClientByHandle(args.handle, session)

  dieIf(not hasattr(client, args.setting_name), 
    "Setting name '" + args.setting_name + "' does not exist.")

  setattr(client, args.setting_name, args.setting_value)
  session.commit()

  print("Client '" + args.handle + "' was updated.")

def commandClientGet(args, session):
  client = getClientByHandle(args.handle, session)

  dieIf(not hasattr(client, args.setting_name), 
    "Setting name '" + args.setting_name + "' does not exist.")

  print(getattr(client, args.setting_name))

def commandClientShow(args, session):
  client = getClientByHandle(args.handle, session)

  table = PrettyTable(['key', 'value'])
  table.align['key'] = 'r'
  table.align['value'] = 'l'
  table.header = False
  table.padding_width = 1

  for key in getClientFields():
    title = getClientFieldTitle(key)
    table.add_row([
      title,
      getattr(client, key)
    ])

  print(table)

def commandClientList(args, session):
  clients = session.query(Client).order_by(Client.client_number, Client.id);
  table = PrettyTable(["Client number", "Handle", "Name"])
  table.padding_width = 1

  for client in clients:
    table.add_row([
      client.client_number if client.client_number else client.id,
      client.handle,
      client.name,
    ])

  print(table)

