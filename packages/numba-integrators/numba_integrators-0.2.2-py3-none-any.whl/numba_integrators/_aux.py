from collections.abc import Callable
from typing import Any
from typing import TypeAlias

import numba as nb
import numpy as np
from numpy.typing import NDArray

# Multiply steps computed from asymptotic behaviour of errors by this.
SAFETY = 0.9

MIN_FACTOR = 0.2  # Minimum allowed decrease in a step size.
MAX_FACTOR = 10  # Maximum allowed increase in a step size.

IS_CACHE = True

# Types

npAFloat64: TypeAlias = NDArray[np.float64]
npAInt64: TypeAlias = NDArray[np.int64]

ODEFUN: TypeAlias  = Callable[[np.float64, npAFloat64], npAFloat64]
ODEFUNA: TypeAlias = Callable[[np.float64, npAFloat64, Any],
                              tuple[npAFloat64, Any]]

# numba types
# ----------------------------------------------------------------------
def nbARO(dim = 1, dtype = nb.float64):
    return nb.types.Array(dtype, dim, 'C', readonly = True)
# ----------------------------------------------------------------------
nbODEsignature = nb.float64[:](nb.float64, nb.float64[:])
nbODEtype = nbODEsignature.as_type()

# ----------------------------------------------------------------------
def nbA(dim = 1, dtype = nb.float64):
    return nb.types.Array(dtype, dim, 'C')
# ----------------------------------------------------------------------
@nb.njit(nb.float64(nb.float64[:]),
         fastmath = True, cache = IS_CACHE)
def norm(x: npAFloat64) -> np.float64:
    """Compute RMS norm."""
    return np.sqrt(np.sum(x * x) / x.size)
