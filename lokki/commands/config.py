import sys

from lokki.db.setting import Setting;
from lokki.config import getValidSettings;

def commandConfigSet(args, session):
  if (not args.setting_name in getValidSettings()):
    sys.stderr.write("Setting name '" + args.setting_name + "' does not exist.\n");
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)

  setting = session.query(Setting).filter_by(name=args.setting_name).first()

  if (not setting):
    setting = Setting()
    setting.name = args.setting_name
    session.add(setting)

  setting.value = args.setting_value

  session.commit()

def commandConfigGet(args, session):
  setting = session.query(Setting).filter_by(name=args.setting_name).first()
  if (not setting):
    print ("Setting was not found.")
  else:
    print (setting.value)

def commandConfigList(args, session):
  for setting in session.query(Setting).order_by(Setting.name): 
    print (setting.name + "=" + setting.value)
