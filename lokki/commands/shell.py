import os
import sys
import subprocess

def commandShell(args, dummy): 
  shell = os.environ['SHELL']
  db_path = args.db_path

  if not os.path.exists(db_path):
    sys.stderr.write("File '" + db_path + "' does not exist.\n")
    sys.exit(1)

  environment = os.environ.copy()
  environment['LK_IS_LK_SESSION'] = '1'
  environment['LK_DB_PATH'] = os.path.abspath(db_path)

  subprocess.call([shell], env=environment)

