import sys

def dieIf(condition, msg):
  if condition:
    sys.stderr.write(msg + "\n")
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)

