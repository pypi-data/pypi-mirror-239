'''
Created on 19.04.2021

@author: fischsam
'''
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.unordered_map cimport unordered_map
cimport numpy as np


cdef extern from "_kde_tools_internals.h":

    cdef cppclass ElementaryLikelihoodComputerBackend[T]:
        ElementaryLikelihoodComputerBackend()
        ElementaryLikelihoodComputerBackend(T **observations_, int *consideredColumns_, int dim_, 
                                            long lenObservations_, T guaranteedLookupDistance_,
                                            int *mode_, T *inverseBandwidth_,
                                            T logNormalization_) except + nogil
        void compute_log_likelihood(T **sample, long lenSample, T *out) except + nogil

ctypedef ElementaryLikelihoodComputerBackend[double] DoubleElementaryLikelihoodComputerBackend
ctypedef ElementaryLikelihoodComputerBackend[float] FloatElementaryLikelihoodComputerBackend

cdef class ElementaryLikelihoodComputer:
    
    cdef: 
        DoubleElementaryLikelihoodComputerBackend doubleElementaryLikelihoodComputerBackend
        FloatElementaryLikelihoodComputerBackend floatElementaryLikelihoodComputerBackend
        np.ndarray observations
        np.ndarray consideredColumns 
        np.ndarray domains
        np.ndarray inverseBandwidth
        np.ndarray weights
        object dtype
        object biasCorrectionFunction
        long columnNumber