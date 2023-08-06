from mpi4py cimport MPI
cdef extern from 'compat.h':
    pass

cdef MPI.Comm comm = MPI.COMM_WORLD

