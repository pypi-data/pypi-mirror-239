import importlib_metadata

try:
    version = importlib_metadata.version("anyllm")
except:
    pass
