import logging

from pypasswork.passwork import PassworkAPI

__all__ = [
    PassworkAPI
]

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
