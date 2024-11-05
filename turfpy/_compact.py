"""
This module is used to check if set variables which
can be used to check whether a dependency is installed
or not.
"""

HAS_PYGEOS = None

HAS_GEOPANDAS = None

HAS_RTREE = None

try:
    import pygeos  # noqa

    HAS_PYGEOS = True
except ImportError:
    HAS_PYGEOS = False


try:
    import geopandas  # noqa

    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False


try:
    import rtree  # noqa

    HAS_RTREE = True
except ImportError:
    HAS_RTREE = False
