from __future__ import absolute_import

try:
    import numpy as _np
    _have_numpy = True
except ImportError:
    _have_numpy = False

from .distob import (scatter, gather, vectorize, apply, call_all, 
                     Remote, proxy_methods, ObjectHub, ObjectEngine, Ref)

engine = None

__version__ = '0.1.5'

if _have_numpy:
    from .arrays import (RemoteArray, DistArray, transpose, rollaxis,
                         expand_dims, concatenate, vstack, hstack, dstack, 
                         split, vsplit, hsplit, dsplit, broadcast_arrays)
