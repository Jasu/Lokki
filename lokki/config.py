from lokki.db.setting import Setting

def getValidSettings(): 
  return [
    'seller-name',
    'seller-address',
    'seller-zip-code',
    'seller-city',
    'seller-country',
    'seller-iban',
    'next-invoice-number',
    'default-due-days',
    'default-client',
    'default-vat',
  ]

def getRequiredSettings(): 
  return [
    'seller-name',
    'seller-address',
    'seller-zip-code',
    'seller-city',
    'seller-iban',
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


