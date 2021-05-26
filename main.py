try:
    from .encode import encode
    from .decode import decode
except ImportError:
    from encode import encode
    from decode import decode