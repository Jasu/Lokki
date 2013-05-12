import os
import subprocess

import pystache

from lokki.db.eventhandler import EventHandler

def triggerEvent(session, eventName, parameters):
  parameters['database_path'] = os.environ['LK_DB_PATH']
  for eventHandler in (session.query(EventHandler)
                       .filter_by(event=eventName)
                       .order_by(EventHandler.index)):
    cmd = pystache.render(eventHandler.command, parameters)
    subprocess.call(cmd, shell=True)

