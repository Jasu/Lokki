import sqlalchemy
import os
import sys
from lokki.db import *

def commandInit(args, dummy):
  db_path = args.db_path

  if (os.path.exists(db_path)):
    sys.stderr.write("File '" + db_path + "' already exists.\n")
    sys.exit(1)

  db = sqlalchemy.create_engine('sqlite:///' + db_path)

  base.Base.metadata.create_all(db)

