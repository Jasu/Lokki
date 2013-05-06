from lokki.util import dieIf

def findSubrow(args, row):
  if args.subrow_index:
    dieIf(int(args.subrow_index) < 1, 
      "Subrow index is too small.")
    dieIf(int(args.subrow_index) > len(row.subrows), 
      "Subrow index is too large.")
    return row.subrows[int(args.subrow_index)]
  else:
    dieIf(len(row.subrows) == 0, "The selected row contains no subrows.")
    return row.subrows[len(row.subrows) - 1]

  
