#!/usr/bin/python

import os
import sys
import argparse
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from pprint import pprint

from lokki.commands.init import commandInit
from lokki.commands.shell import commandShell

lokki_dir = os.path.dirname(os.path.abspath(__file__))

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
  commandInvoiceUnbill,
  commandInvoiceMerge,
  commandInvoiceGenerate
  )

from lokki.commands.row import (
  commandRowAdd, 
  commandRowRemove, 
  commandRowSet, 
  commandRowGet,
  commandRowMv
  )

from lokki.commands.composite import (
  commandCompositeAdd, 
  commandCompositeRemove, 
  commandCompositeShow,
  commandCompositeMerge
  )

from lokki.commands.subrow import (
  commandSubrowAdd, 
  commandSubrowRemove, 
  commandSubrowSet, 
  commandSubrowGet,
  commandSubrowMv
  )

from lokki.commands.event import (
  commandEventAdd, 
  commandEventRemove, 
  commandEventSet, 
  commandEventGet,
  commandEventList
  )

from lokki.commands.external import (
  commandExternalRows,
  commandExternalSubrows
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
clientAddSubcommandParser.add_argument('--name', 
                                       help='Name', 
                                       required=False)
clientAddSubcommandParser.add_argument('--address', 
                                       help='Street address', 
                                       required=False)
clientAddSubcommandParser.add_argument('--address_2', 
                                       help='Street address, second line', 
                                       required=False)
clientAddSubcommandParser.add_argument('--zip_code', 
                                       help='ZIP code', 
                                       required=False)
clientAddSubcommandParser.add_argument('--city', 
                                       help='City', 
                                       required=False)
clientAddSubcommandParser.add_argument('--country', 
                                       help='Country', 
                                       required=False)
clientAddSubcommandParser.add_argument('--client_number', 
                                       help='Client number', 
                                       required=False)
clientAddSubcommandParser.add_argument('--company_number', 
                                       help='Local company number', 
                                       required=False)
clientAddSubcommandParser.add_argument('--vat_number', 
                                       help='European VAT number', 
                                       required=False)

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
invoiceAddSubcommandParser.add_argument('--json', help='As output, print the invoice as json.', required=False, action='store_true')
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
invoiceShowSubcommandParser.add_argument('--json', help='As output, print the invoice as json.', required=False, action='store_true')
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

invoiceUnbillSubcommandParser = invoiceSubcommandSubParsers.add_parser('merge')
invoiceUnbillSubcommandParser.add_argument('source_invoice_number', help='Source invoice number')
invoiceUnbillSubcommandParser.add_argument('target_invoice_number', help='Target invoice number')
invoiceUnbillSubcommandParser.set_defaults(func=commandInvoiceMerge)

invoiceGenerateSubcommandParser = (
  invoiceSubcommandSubParsers.add_parser('generate'))
invoiceGenerateSubcommandParser.add_argument('--filename', 
                                             help='Output file', 
                                             required=False)
invoiceGenerateSubcommandParser.add_argument('--template', 
                                             help='Template file', 
                                             required=False)
invoiceGenerateSubcommandParser.add_argument('--hide-details', 
                                             help='If set, hides the composite'
                                                  ' row details', 
                                             action='store_true')
invoiceGenerateSubcommandParser.add_argument('invoice_number', 
                                             help='Invoice number', 
                                             nargs='?')
invoiceGenerateSubcommandParser.set_defaults(func=commandInvoiceGenerate)

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
rowAddSubcommandParser.add_argument('--json', help='As output, display the row in JSON.', required=False, action='store_true')
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

rowMvSubcommandParser = rowSubcommandSubParsers.add_parser('mv')
rowMvSubcommandParser.set_defaults(func=commandRowMv)
rowMvSubcommandParser.add_argument('src_invoice_number', help='Source invoice number')
rowMvSubcommandParser.add_argument('dst_invoice_number', help='Destination invoice number')
rowMvSubcommandParser.add_argument('row', help='Row index')

###############################################################################
# COMMAND composite                                                           #
###############################################################################

compositeSubcommandParser = subcommandParsers.add_parser('composite')
compositeSubcommandSubParsers = compositeSubcommandParser.add_subparsers(
                                title='composite row commands')

compositeAddSubcommandParser = compositeSubcommandSubParsers.add_parser('add')
compositeAddSubcommandParser.set_defaults(func=commandCompositeAdd)
compositeAddSubcommandParser.add_argument('title', help='Title')
compositeAddSubcommandParser.add_argument('--json', help='As output, display the row in JSON.', required=False, action='store_true')
compositeAddSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
compositeAddSubcommandParser.add_argument('--vat', help='VAT, eg. "22%" or "0.22".', required=False)
compositeAddSubcommandParser.add_argument('--note', help='A descriptive longer note to display on the invoice.', required=False)
compositeAddSubcommandParser.add_argument('--external_source', help='When importing from an external system, an identification string of the system.', required=False)
compositeAddSubcommandParser.add_argument('--external_id', help='When importing from an external system, ID of the composite row in the other system', required=False)

compositeRemoveSubcommandParser = compositeSubcommandSubParsers.add_parser('remove')
compositeRemoveSubcommandParser.set_defaults(func=commandCompositeRemove)
compositeRemoveSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
compositeRemoveSubcommandParser.add_argument('index', help='Composite index')

compositeShowSubcommandParser = compositeSubcommandSubParsers.add_parser('show')
compositeShowSubcommandParser.set_defaults(func=commandCompositeShow)
compositeShowSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
compositeShowSubcommandParser.add_argument('index', help='Composite index')

compositeShowSubcommandParser = compositeSubcommandSubParsers.add_parser('merge')
compositeShowSubcommandParser.set_defaults(func=commandCompositeMerge)
compositeShowSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
compositeShowSubcommandParser.add_argument('source_index', help='Source row index')
compositeShowSubcommandParser.add_argument('target_index', help='Target row index')

###############################################################################
# COMMAND subrow                                                              #
###############################################################################

subrowSubcommandParser = subcommandParsers.add_parser('subrow')
subrowSubcommandSubParsers = subrowSubcommandParser.add_subparsers(
                                title='subrow commands')

subrowAddSubcommandParser = subrowSubcommandSubParsers.add_parser('add')
subrowAddSubcommandParser.set_defaults(func=commandSubrowAdd)
subrowAddSubcommandParser.add_argument('title', help='Title')
subrowAddSubcommandParser.add_argument('price_per_unit', help='Price per unit')
subrowAddSubcommandParser.add_argument('num_units', help='Number of units', nargs='?')
subrowAddSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
subrowAddSubcommandParser.add_argument('--row', help='Composite row index', required=False)
subrowAddSubcommandParser.add_argument('--note', help='A descriptive longer note to display on the invoice.', required=False)
subrowAddSubcommandParser.add_argument('--external_source', help='When importing from an external system, an identification string of the system.', required=False)
subrowAddSubcommandParser.add_argument('--external_id', help='When importing from an external system, ID of the subrow in the other system', required=False)

subrowRemoveSubcommandParser = subrowSubcommandSubParsers.add_parser('remove')
subrowRemoveSubcommandParser.set_defaults(func=commandSubrowRemove)
subrowRemoveSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
subrowRemoveSubcommandParser.add_argument('--row', help='Composite row index', required=False)
subrowRemoveSubcommandParser.add_argument('--vat', help='VAT, eg. "22%" or "0.22".', required=False)
subrowRemoveSubcommandParser.add_argument('--note', help='A descriptive longer note to display on the invoice.', required=False)
subrowRemoveSubcommandParser.add_argument('--external_source', help='When importing from an external system, an identification string of the system.', required=False)
subrowRemoveSubcommandParser.add_argument('--external_id', help='When importing from an external system, ID of the subrow in the other system', required=False)
subrowRemoveSubcommandParser.add_argument('subrow_index', help='Subrow index', nargs='?')

subrowSetSubcommandParser = subrowSubcommandSubParsers.add_parser('set')
subrowSetSubcommandParser.set_defaults(func=commandSubrowSet)
subrowSetSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
subrowSetSubcommandParser.add_argument('--row', help='Composite row number', required=False)
subrowSetSubcommandParser.add_argument('subrow_index', help='Subrow index', nargs='?')
subrowSetSubcommandParser.add_argument('setting_name', help='Setting name')
subrowSetSubcommandParser.add_argument('setting_value', help='Setting value')

subrowGetSubcommandParser = subrowSubcommandSubParsers.add_parser('get')
subrowGetSubcommandParser.set_defaults(func=commandSubrowGet)
subrowGetSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
subrowGetSubcommandParser.add_argument('--row_number', help='Composite row number', required=False)
subrowGetSubcommandParser.add_argument('index', help='Subrow index', nargs='?')
subrowGetSubcommandParser.add_argument('setting_name', help='Setting name')

subrowMvSubcommandParser = subrowSubcommandSubParsers.add_parser('mv')
subrowMvSubcommandParser.set_defaults(func=commandSubrowMv)
subrowMvSubcommandParser.add_argument('--invoice_number', help='Invoice number', required=False)
subrowMvSubcommandParser.add_argument('src_row_index', help='Source composite row index')
subrowMvSubcommandParser.add_argument('dst_row_index', help='Destination composite row index')
subrowMvSubcommandParser.add_argument('subrow_index', help='Subrow index')

###############################################################################
# COMMAND event                                                               #
###############################################################################

eventSubcommandParser = subcommandParsers.add_parser('event')
eventSubcommandSubParsers = eventSubcommandParser.add_subparsers(
                                title='event commands')

eventAddSubcommandParser = eventSubcommandSubParsers.add_parser('add')
eventAddSubcommandParser.set_defaults(func=commandEventAdd)
eventAddSubcommandParser.add_argument('event', help='Event name')
eventAddSubcommandParser.add_argument('command', help='Command')

eventRemoveSubcommandParser = eventSubcommandSubParsers.add_parser('remove')
eventRemoveSubcommandParser.set_defaults(func=commandEventRemove)
eventRemoveSubcommandParser.add_argument('--event', 
                                         help='Event name', 
                                         nargs='?')
eventRemoveSubcommandParser.add_argument('--index', 
                                         help='Event index', 
                                         nargs='?')
eventRemoveSubcommandParser.add_argument('--id', 
                                         help='Event id', 
                                         nargs='?')

eventSetSubcommandParser = eventSubcommandSubParsers.add_parser('set')
eventSetSubcommandParser.set_defaults(func=commandEventSet)
eventSetSubcommandParser.add_argument('--event', 
                                      help='Event name', 
                                      nargs='?')
eventSetSubcommandParser.add_argument('--index', 
                                      help='Event index', 
                                      nargs='?')
eventSetSubcommandParser.add_argument('--id', 
                                      help='Event id', 
                                      nargs='?')
eventSetSubcommandParser.add_argument('setting_name', help='Setting name')
eventSetSubcommandParser.add_argument('setting_value', help='Setting value')

eventGetSubcommandParser = eventSubcommandSubParsers.add_parser('get')
eventGetSubcommandParser.set_defaults(func=commandEventGet)
eventGetSubcommandParser.add_argument('--event', 
                                      help='Event name', 
                                      nargs='?')
eventGetSubcommandParser.add_argument('--index', 
                                      help='Event index', 
                                      nargs='?')
eventGetSubcommandParser.add_argument('--id', 
                                      help='Event id', 
                                      nargs='?')
eventGetSubcommandParser.add_argument('setting_name', help='Setting name')

eventListSubcommandParser = eventSubcommandSubParsers.add_parser('list')
eventListSubcommandParser.set_defaults(func=commandEventList)
eventListSubcommandParser.add_argument('--event', 
                                       help='Event name', 
                                       nargs='?')

###############################################################################
# COMMAND external                                                            #
###############################################################################

externalSubcommandParser = subcommandParsers.add_parser('external')
externalSubcommandSubParsers = externalSubcommandParser.add_subparsers(
                                title='external (interfacing) commands')

externalRowsSubcommandParser = externalSubcommandSubParsers.add_parser('rows')
externalRowsSubcommandParser.set_defaults(func=commandExternalRows)
externalRowsSubcommandParser.add_argument('--json', help='As output, display the row map in JSON.', required=False, action='store_true')
externalRowsSubcommandParser.add_argument('--external_source', help='Filter by a specific source.', required=False)

externalSubrowsSubcommandParser = externalSubcommandSubParsers.add_parser('subrows')
externalSubrowsSubcommandParser.set_defaults(func=commandExternalSubrows)
externalSubrowsSubcommandParser.add_argument('--json', help='As output, display the subrow map in JSON.', required=False, action='store_true')
externalSubrowsSubcommandParser.add_argument('--external_source', help='Filter by a specific source.', required=False)

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

