from collections import namedtuple, defaultdict
import numpy as np
from ..constants import BLOCK_SIZE_BYTES

Field = namedtuple("Field", ["position", "name", "unit", "shape", "dtype"])

# set default for unit, shape, and dtype, thus works for the 3 right most attributes
Field.__new__.__defaults__ = (None, 1, "f4")


def build_dtype(fields, itemsize = BLOCK_SIZE_BYTES):
    dt = defaultdict(list)

    if itemsize is not None:
        dt["itemsize"] = itemsize

    for field in fields:
        dt["names"].append(field.name)
        dt["offsets"].append((field.position - 1) * 4)
        if field.shape != 1:
            dt["formats"].append((field.dtype, field.shape))
        else:
            dt["formats"].append(field.dtype)

    return np.dtype(dict(**dt))