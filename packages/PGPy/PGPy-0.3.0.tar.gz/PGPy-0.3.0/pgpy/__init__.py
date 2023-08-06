""" PGPy :: Pretty Good Privacy for Python
"""
from ._author import __author__
from ._author import __copyright__
from ._author import __license__
from ._author import __version__

from . import constants
from . import errors

from .pgp import PGPKey
from .pgp import PGPKeyring
from .pgp import PGPMessage
from .pgp import PGPSignature
from .pgp import PGPUID

__all__ = [__author__,
           __copyright__,
           __license__,
           __version__,
           constants,
           errors,
           PGPKey,
           PGPKeyring,
           PGPMessage,
           PGPSignature,
           PGPUID
           ]
