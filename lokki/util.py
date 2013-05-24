import sys
from decimal import Decimal, ROUND_HALF_UP

def dieIf(condition, msg):
  if condition:
    sys.stderr.write(msg + "\n")
    sys.stderr.write("Nothing done.\n")
    sys.exit(1)


def formatNumber(number):
  if isinstance(number, str):
    number = Decimal(number)
  return str(number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)).replace('.', ',')

