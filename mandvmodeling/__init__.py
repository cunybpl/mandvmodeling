from ._version import VERSION

__version__ = VERSION

from mandvmodeling.core import calc, estimator, schemas

__all__ = ["calc", "estimator", "schemas"]
