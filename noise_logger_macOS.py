# ========================================================================
# Parche noise_logger_macOS.py
# Parche global para bibliotecas librtlsdr antiguas en macOS / Python 3.14
# incluir al principio de noise_logger.py 
# =========================================================================

import ctypes

_original_getitem = ctypes.CDLL.__getitem__

def _patched_getitem(self, name_or_ordinal):
    try:
        return _original_getitem(self, name_or_ordinal)
    except AttributeError:
        # Si la función C no existe en el sistema, devuelve una función dummy que no rompe el programa
        return ctypes.CFUNCTYPE(ctypes.c_int)(lambda *args: 0)

ctypes.CDLL.__getitem__ = _patched_getitem

# =========================================================================
