import numpy as np
import numpy.ctypeslib as npct
import ctypes
import os.path

array_1d_float = npct.ndpointer(dtype=np.dtype('float64'), ndim=1, flags='CONTIGUOUS')
array_2d_char = npct.ndpointer(dtype=np.dtype('uint8'), ndim=2, flags='CONTIGUOUS')

libcd = npct.load_library('libcd', os.path.join(os.path.dirname(__file__), '_build'))

libcd.sample_sequences.restype = None
libcd.sample_sequences.argtypes = [
    array_2d_char,     # *msa
    array_1d_float,    # *x
    ctypes.c_uint64,    # nrow
    ctypes.c_uint32,    # ncol
]


def sample_sequences(msa, x):
    libcd.sample_sequences(msa, x, *msa.shape)
    return msa
