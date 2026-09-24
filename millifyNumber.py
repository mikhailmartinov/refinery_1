import math
from decimal import Decimal


def removeExponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def millify(n, precision=0, dropNulls=True, prefixes=[]):
    millNames = ['', 'k', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if prefixes:
        millNames = ['']
        millNames.extend(prefixes)
    n = float(n)
    millIdx = max(0, min(len(millNames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    result = '{:.{precision}f}'.format(n / 10**(3 * millIdx), precision=precision)
    if dropNulls:
        result = removeExponent(Decimal(result))
    return '{0}{dx}'.format(result, dx=millNames[millIdx])
