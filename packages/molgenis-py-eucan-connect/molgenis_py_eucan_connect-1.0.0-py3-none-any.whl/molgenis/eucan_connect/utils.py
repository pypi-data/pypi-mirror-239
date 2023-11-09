from collections import OrderedDict
from typing import List


def to_ordered_dict(rows: List[dict]) -> OrderedDict:
    rows_by_id = OrderedDict()
    for row in rows:
        rows_by_id[row["id"]] = row
    return rows_by_id


def isnan(value):
    # A NaN implemented following the standard, is the only value for which
    # the inequality comparison with itself should return True:
    return value != value
