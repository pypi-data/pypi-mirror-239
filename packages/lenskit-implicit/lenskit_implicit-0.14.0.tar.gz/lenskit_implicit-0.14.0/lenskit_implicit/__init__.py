"""
LensKit wrappers for the Implicit package.
"""

from . import _pt
__version__ = '0.14.0'
__version__ = _pt.gitify_version(__version__)

if __name__ == 'lenskit_implicit':
    from .implicit import *  # noqa: F401
