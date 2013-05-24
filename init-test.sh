#!/bin/sh

lk config set seller-name "ACME Inc. & Co. Ltd. GmbH"
lk config set seller-address "Seller's Street 21"
lk config set seller-zip-code "01234"
lk config set seller-city "New York"
lk config set seller-phone-number "800-555-0199"
lk config set seller-company-number "1234567-8"
lk config set seller-iban "FI00 0000 0000 0000 01"
lk config set seller-bank "MoneyHole"
lk config set seller-bic "BICBICBI"
lk config set default-vat 0.24
lk config set default-due-days 14
lk config set next-invoice-number 1
lk config set default-invoice-template tpl/default.html
lk config set invoice-filename-template 'test-{{y}}-{{m}}-{{d}}-{{n}}.html'

lk client add test
lk client set test name "BallMart Ltd."
lk client set test address "Buyer's Street 99"
lk client set test zip_code "70000"
lk client set test city "London"
lk client set test company_number "2345678-9"

lk config set default-client 1

