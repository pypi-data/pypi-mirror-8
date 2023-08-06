"""oTree Public API utilities"""

from easymoney import Money as Currency, to_dec
from django.utils.safestring import mark_safe
import json

class _CurrencyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Currency):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def safe_json(obj):
    return mark_safe(json.dumps(obj, cls=_CurrencyEncoder))

# FIXME: there is a problem with currency = 0.01. this increment is too small if you use points.
# causes the function to hang.
def currency_range(first, last, increment):
    assert last >= first
    assert increment >= 0
    values = []
    current_value = Currency(first)
    while True:
        if current_value > last:
            return values
        values.append(current_value)
        current_value += increment
