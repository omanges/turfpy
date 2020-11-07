HAS_PYGEOS = None

HAS_GEOPANDAS = None


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
