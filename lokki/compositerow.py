from lokki.util import dieIf

def findSubrow(row, subrowIndex):
    if subrowIndex:
        dieIf(int(subrowIndex) < 1, 
              "Subrow index is too small.")
        dieIf(int(subrowIndex) > len(row.subrows), 
              "Subrow index is too large.")
        return row.subrows[int(subrowIndex) - 1]
    else:
        dieIf(len(row.subrows) == 0, "The selected row contains no subrows.")
        return row.subrows[len(row.subrows) - 1]

