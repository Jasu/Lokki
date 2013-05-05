#!/usr/bin/python

import os
import sys
import argparse
import sqlalchemy
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lokki.commands.init import commandInit
from lokki.commands.shell import commandShell

from lokki.commands.config import (
  commandConfigSet, 
  commandConfigGet, 
  commandConfigList
  )

from lokki.commands.client import (
  commandClientAdd, 
  commandClientRemove, 
  commandClientList, 
  commandClientSet, 
  commandClientGet, 
  commandClientShow
  )

from lokki.commands.invoice import (
  commandInvoiceAdd, 
  commandInvoiceRemove, 
  commandInvoiceSet, 
  commandInvoiceGet, 
  commandInvoiceShow, 
  commandInvoiceList, 
  commandInvoiceBill, 
  commandInvoiceUnbill
  )

from lokki.commands.row import (
  commandRowAdd, 
  commandRowRemove, 
  commandRowSet, 
  commandRowGet
  )

commandLineParser = argparse.ArgumentParser(
                      description='Lokki - command line billing')

subcommandParsers = commandLineParser.add_subparsers(
                      title='Subcommands',
                      description='valid subcommands')

###############################################################################
# COMMAND shell                                                               #
###############################################################################

shellSubcommandParser = subcommandParsers.add_parser('shell')
shellSubcommandParser.set_defaults(func=commandShell)
shellSubcommandParser.add_argument('db_path', help='SQLite database to use.')

###############################################################################
# COMMAND init                                                                #
###############################################################################

initSubcommandParser = subcommandParsers.add_parser('init')
initSubcommandParser.set_defaults(func=commandInit)
initSubcommandParser.add_argument('db_path', 
  help='SQLite database to init. The file must not exist.')

###############################################################################
# COMMAND config                                                              #
###############################################################################

configSubcommandParser = subcommandParsers.add_parser('config')
configSubcommandSubParsers = configSubcommandParser.add_subparsers(
                                title='Configuration commands')

configSetSubcommandParser = configSubcommandSubParsers.add_parser('set')
configSetSubcommandParser.set_defaults(func=commandConfigSet)
configSetSubcommandParser.add_argument('setting_name', help='Setting name')
configSetSubcommandParser.add_argument('setting_value', help='Setting value')

configRemoveSubcommandParser = configSubcommandSubParsers.add_parser('get')
configRemoveSubcommandParser.set_defaults(func=commandConfigGet)
configRemoveSubcommandParser.add_argument('setting_name', help='Setting name')

configListSubcommandParser = configSubcommandSubParsers.add_parser('list')
configListSubcommandParser.set_defaults(func=commandConfigList)

###############################################################################
# COMMAND client                                                              #
###############################################################################

clientSubcommandParser = subcommandParsers.add_parser('client')
clientSubcommandSubParsers = clientSubcommandParser.add_subparsers(
                                title='client commands')

clientAddSubcommandParser = clientSubcommandSubParsers.add_parser('add')
clientAddSubcommandParser.set_defaults(func=commandClientAdd)
clientAddSubcommandParser.add_argument('handle', help='Client handle')
clientAddSubcommandParser.add_argument('name', help='Name', nargs='?')
clientAddSubcommandParser.add_argument('address', help='Street address', nargs='?')
clientAddSubcommandParser.add_argument('zip_code', help='ZIP code', nargs='?')
clientAddSubcommandParser.add_argument('city', help='City', nargs='?')
clientAddSubcommandParser.add_argument('country', help='Country', nargs='?')
clientAddSubcommandParser.add_argument('client_number', help='Client number', nargs='?')

clientRemoveSubcommandParser = clientSubcommandSubParsers.add_parser('remove')
clientRemoveSubcommandParser.set_defaults(func=commandClientRemove)
clientRemoveSubcommandParser.add_argument('handle', help='Client handle')

clientSetSubcommandParser = clientSubcommandSubParsers.add_parser('set')
clientSetSubcommandParser.set_defaults(func=commandClientSet)
clientSetSubcommandParser.add_argument('handle', help='Client handle')
clientSetSubcommandParser.add_argument('setting_name', help='Setting name')
clientSetSubcommandParser.add_argument('setting_value', help='Setting value')

clientGetSubcommandParser = clientSubcommandSubParsers.add_parser('get')
clientGetSubcommandParser.set_defaults(func=commandClientGet)
clientGetSubcommandParser.add_argument('handle', help='Client handle')
clientGetSubcommandParser.add_argument('setting_name', help='Setting name')

clientShowSubcommandParser = clientSubcommandSubParsers.add_parser('show')
clientShowSubcommandParser.set_defaults(func=commandClientShow)
clientShowSubcommandParser.add_argument('handle', help='Client handle')

clientListSubcommandParser = clientSubcommandSubParsers.add_parser('list')
clientListSubcommandParser.set_defaults(func=commandClientList)


###############################################################################
# COMMAND invoice                                                             #
###############################################################################

invoiceSubcommandParser = subcommandParsers.add_parser('invoice')
invoiceSubcommandSubParsers = invoiceSubcommandParser.add_subparsers(
                                title='invoice commands')

invoiceAddSubcommandParser = invoiceSubcommandSubParsers.add_parser('add')
invoiceAddSubcommandParser.set_defaults(func=commandInvoiceAdd)
invoiceAddSubcommandParser.add_argument('--client_handle', help='Client handle', required=False)
invoiceAddSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
invoiceAddSubcommandParser.add_argument('--date', help='Date', required=False)
invoiceAddSubcommandParser.add_argument('--duedate', help='Due date', required=False)
invoiceAddSubcommandParser.add_argument('--duedays', help='Days to due from date', required=False)

invoiceRemoveSubcommandParser = invoiceSubcommandSubParsers.add_parser('remove')
invoiceRemoveSubcommandParser.set_defaults(func=commandInvoiceRemove)
invoiceRemoveSubcommandParser.add_argument('invoice_number', help='Invoice number')

invoiceSetSubcommandParser = invoiceSubcommandSubParsers.add_parser('set')
invoiceSetSubcommandParser.set_defaults(func=commandInvoiceSet)
invoiceSetSubcommandParser.add_argument('invoice_number', help='Invoice number', nargs='?')
invoiceSetSubcommandParser.add_argument('setting_name', help='Setting name')
invoiceSetSubcommandParser.add_argument('setting_value', help='Setting value')

invoiceGetSubcommandParser = invoiceSubcommandSubParsers.add_parser('get')
invoiceGetSubcommandParser.set_defaults(func=commandInvoiceGet)
invoiceGetSubcommandParser.add_argument('invoice_number', help='Invoice number', nargs='?')
invoiceGetSubcommandParser.add_argument('setting_name', help='Setting name')

invoiceShowSubcommandParser = invoiceSubcommandSubParsers.add_parser('show')
invoiceShowSubcommandParser.set_defaults(func=commandInvoiceShow)
invoiceShowSubcommandParser.add_argument('invoice_number', help='Invoice number', nargs='?')

invoiceListSubcommandParser = invoiceSubcommandSubParsers.add_parser('list')
invoiceListSubcommandParser.add_argument('--client_handle', help='Client handle', required=False)
invoiceListSubcommandParser.set_defaults(func=commandInvoiceList)

invoiceBillSubcommandParser = invoiceSubcommandSubParsers.add_parser('bill')
invoiceBillSubcommandParser.add_argument('invoice_number', help='Invoice number', nargs='?')
invoiceBillSubcommandParser.set_defaults(func=commandInvoiceBill)

invoiceUnbillSubcommandParser = invoiceSubcommandSubParsers.add_parser('unbill')
invoiceUnbillSubcommandParser.add_argument('invoice_number', help='Invoice number', nargs='?')
invoiceUnbillSubcommandParser.set_defaults(func=commandInvoiceUnbill)

###############################################################################
# COMMAND row                                                                 #
###############################################################################

rowSubcommandParser = subcommandParsers.add_parser('row')
rowSubcommandSubParsers = rowSubcommandParser.add_subparsers(
                                title='row commands')

rowAddSubcommandParser = rowSubcommandSubParsers.add_parser('add')
rowAddSubcommandParser.set_defaults(func=commandRowAdd)
rowAddSubcommandParser.add_argument('title', help='Title')
rowAddSubcommandParser.add_argument('price_per_unit', help='Price per unit')
rowAddSubcommandParser.add_argument('num_units', help='Number of units', nargs='?')
rowAddSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
rowAddSubcommandParser.add_argument('--vat', help='VAT, eg. "22%" or "0.22".', required=False)
rowAddSubcommandParser.add_argument('--note', help='A descriptive longer note to display on the invoice.', required=False)
rowAddSubcommandParser.add_argument('--external_source', help='When importing from an external system, an identification string of the system.', required=False)
rowAddSubcommandParser.add_argument('--external_id', help='When importing from an external system, ID of the row in the other system', required=False)

rowRemoveSubcommandParser = rowSubcommandSubParsers.add_parser('remove')
rowRemoveSubcommandParser.set_defaults(func=commandRowRemove)
rowRemoveSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
rowRemoveSubcommandParser.add_argument('index', help='Row index')

rowSetSubcommandParser = rowSubcommandSubParsers.add_parser('set')
rowSetSubcommandParser.set_defaults(func=commandRowSet)
rowSetSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
rowSetSubcommandParser.add_argument('index', help='Row index')
rowSetSubcommandParser.add_argument('setting_name', help='Setting name')
rowSetSubcommandParser.add_argument('setting_value', help='Setting value')

rowGetSubcommandParser = rowSubcommandSubParsers.add_parser('get')
rowGetSubcommandParser.set_defaults(func=commandRowGet)
rowGetSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
rowGetSubcommandParser.add_argument('index', help='Row index')
rowGetSubcommandParser.add_argument('setting_name', help='Setting name')

###############################################################################
# Connect to database                                                         #
###############################################################################

db = None
session = None
if 'LK_DB_PATH' in os.environ:
  db = sqlalchemy.create_engine('sqlite:///' + os.environ['LK_DB_PATH'])
  session = sessionmaker(bind=db, autoflush=False)()

###############################################################################
# Invoke the command                                                          #
###############################################################################

arguments = commandLineParser.parse_args()
if ('func' in arguments):
  arguments.func(arguments, session)
else:
  commandLineParser.print_help()

