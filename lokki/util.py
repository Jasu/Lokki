import sys
from decimal import Decimal

def dieIf(condition, msg):
  if condition:
    sys.stderr.write(msg + "\n")
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)


def formatNumber(number):
  if isinstance(number, str):
    number = Decimal(number)
  return str(number.quantize(Decimal('.01'))).replace('.', ',')
