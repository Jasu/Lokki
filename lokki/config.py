def getValidSettings(): 
  return [
    'seller-name',
    'seller-address',
    'seller-zip-code',
    'seller-city',
    'seller-country',
    'next-invoice-number',
    'default-due-days',
    'default-recipient',
    'default-vat',
  ]

def getRequiredSettings(): 
  return [
    'seller-name',
    'seller-address',
    'seller-zip-code',
    'seller-city',
  ]

def getConfiguration(session):
  result = {}
  for setting in session.query(Setting).order_by(Setting.name): 
    result[setting.name] = setting.value

def isConfigurationValid(session):
  configuration = getConfiguration(session)
  required = getRequiredSettings()

  for settingName in required:
    if (not settingName in configuration):
      return False

  return True

