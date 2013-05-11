from lokki.db.setting import Setting
import sys

def getValidSettings(): 
  return [
    'seller-name',
    'seller-vat-number',
    'seller-company-number',
    'seller-address',
    'seller-address-2',
    'seller-zip-code',
    'seller-city',
    'seller-country',
    'seller-phone-number',
    'seller-iban',
    'seller-bank',
    'seller-bic',
    'next-invoice-number',
    'default-due-days',
    'default-client',
    'default-vat',
    'default-invoice-template',
    'invoice-filename-template'
  ]

def getRequiredSettings(): 
  return [
    'seller-name',
    'seller-address',
    'seller-zip-code',
    'seller-city',
    'seller-phone-number',
    'seller-company-number',
    'seller-iban',
    'seller-bank',
    'seller-bic',
  ]

def getConfiguration(session):
  result = {}
  for setting in session.query(Setting).order_by(Setting.name): 
    result[setting.name] = setting.value
  return result

def isConfigurationValid(session):
  configuration = getConfiguration(session)
  required = getRequiredSettings()

  for settingName in required:
    if not settingName in configuration:
      return False

  return True

def getSetting(session, settingName):
  setting = session.query(Setting).filter_by(name=settingName).first()
  if setting:
    return setting.value
  else:
    return None


