# distutils: language=c++
#cython: language_level=3, boundscheck=False, wraparound=False, nonecheck=False
'''
Created on 19.04.2021

@author: fischsam
'''


from cython import nogil

import numpy as np

cimport numpy as np
from libc.stdlib cimport malloc, free

#needed to initialize PyArray_API in order to be able to use it
np.import_array()

def _check_dim(np.ndarray arr, dim, name="Array"):
    if not arr.ndim == dim:
        raise ValueError(name + " does not have the right dimension ({})".format(dim))


cdef double** double_arr_to_ptr(np.ndarray[double, ndim=2] array):
    cdef double **result 
    result = <double **> malloc(sizeof(result[0]) * array.shape[0])
    for i in range(array.shape[0]):
        result[i] = <double *> &array[i, 0]
    
    return result

cdef float** float_arr_to_ptr(np.ndarray[float, ndim=2] array):
    cdef float **result 
    result = <float **> malloc(sizeof(result[0]) * array.shape[0])
    for i in range(array.shape[0]):
        result[i] = <float *> &array[i, 0]
    
    return result
    

cdef class ElementaryLikelihoodComputer():
    
    def __init__(self, 
            np.ndarray observations, 
            np.ndarray weights, 
            np.ndarray consideredColumns, 
            np.ndarray domains, 
            np.ndarray inverseBandwidth, 
            double logNormalization,
            double guaranteedLookupDistance,
            biasCorrectionFunction=None,
            dtype=None):
        
        _check_dim(observations, 2, "'observations'")
        _check_dim(weights, 1, "'weights'")
        _check_dim(consideredColumns, 1, "'consideredColumns'")
        _check_dim(domains, 1, "'domains'")
        _check_dim(inverseBandwidth, 1, "'inverseBandwidth'")
        
        rowNumber = observations.shape[0]
        self.columnNumber = columnNumber = observations.shape[1]
        
        if not weights.size == rowNumber:
            raise ValueError("Size of weights does not match "
                             "dimension 2 of observations ({})".format(rowNumber))
        if not inverseBandwidth.size == columnNumber:
            raise ValueError("Size of inverseBandwidth does not match "
                             "dimension 1 of observations ({})".format(columnNumber))
        if not domains.size == columnNumber:
            raise ValueError("Size of domains does not match "
                             "dimension 1 of observations ({})".format(columnNumber))
        if not consideredColumns.size:
            raise ValueError("consideredColumns must contain at least one value.")
        if (consideredColumns >= columnNumber).any() or (consideredColumns < 0).any():
            raise ValueError("consideredColumns must contain nonnegative integers below "
                             "dimension 1 of observations ({})".format(columnNumber))
        if (inverseBandwidth <= 0).any():
            raise ValueError("inverseBandwidth must contain positive values only.")
        if guaranteedLookupDistance <= 0:
            raise ValueError("guaranteedLookupDistance must be positive.")
        
        if dtype: 
            if dtype not in [np.float32, np.float64]:
                raise ValueError("The data type must be either np.float32 or np.float64")
            self.dtype = dtype
        else:
            if observations.dtype == np.float32:
                self.dtype = np.float32
            else:
                self.dtype = np.float64
    
        self.observations = observations.astype(self.dtype, order='C', copy=False)
        self.weights = weights.astype(self.dtype, order='C', copy=False)
        
        self.consideredColumns = consideredColumns.astype(np.int32, order='C', copy=False)
        self.domains = domains.astype(np.int32, order='C', copy=False)
        self.inverseBandwidth = inverseBandwidth.astype(self.dtype, order='C', copy=False)
        self.biasCorrectionFunction = biasCorrectionFunction
        
        cdef:
            int* domainsData = <int*> self.domains.data
            float* floatInverseBandwidthData
            double* doubleInverseBandwidthData
            float** floatObservationsData
            double** doubleObservationsData
            int consideredColumnsSize = self.consideredColumns.size
            int* consideredColumnsData = <int*> self.consideredColumns.data
            long observationNumber = self.observations.shape[0] 
        
        if self.dtype == np.float32:
            floatInverseBandwidthData = <float*> self.inverseBandwidth.data
            floatObservationsData = float_arr_to_ptr(self.observations)
            with nogil:
                self.floatElementaryLikelihoodComputerBackend = FloatElementaryLikelihoodComputerBackend(
                    floatObservationsData,
                    consideredColumnsData,
                    consideredColumnsSize,
                    observationNumber,
                    guaranteedLookupDistance,
                    domainsData,
                    floatInverseBandwidthData,
                    logNormalization
                )

        elif self.dtype == np.float64:
            doubleInverseBandwidthData = <double*> self.inverseBandwidth.data
            doubleObservationsData = double_arr_to_ptr(self.observations)
            with nogil:
                self.doubleElementaryLikelihoodComputerBackend = DoubleElementaryLikelihoodComputerBackend(
                    doubleObservationsData,
                    consideredColumnsData,
                    consideredColumnsSize,
                    observationNumber,
                    guaranteedLookupDistance,
                    domainsData,
                    doubleInverseBandwidthData,
                    logNormalization
                )
        else:
            raise ValueError("Data type not understood. This should not have happened.")
        
    def compute_log_likelihood(self, np.ndarray sample):
        cdef:
            float **sampleFloatPointer
            double **sampleDoublePointer
            np.ndarray out
            
        _check_dim(sample, 2, "'sample'")
        
        if not sample.shape[1] == self.columnNumber:
            raise ValueError("sample does not match observations along axis 1 ({})".format(self.columnNumber))
        
        sample = sample.astype(self.dtype, order='C', copy=False)
        out = np.zeros(self.observations.shape[0], dtype=self.dtype)
        
        cdef: 
            float* floatOutData
            double* doubleOutData
            long sampleSize = sample.shape[0] 
        
        if self.dtype == np.float32:
            sampleFloatPointer = float_arr_to_ptr(sample)
            floatOutData = <float*> out.data
            with nogil:
                self.floatElementaryLikelihoodComputerBackend.compute_log_likelihood(
                    sampleFloatPointer, sampleSize, floatOutData
                )
                free(sampleFloatPointer)
        else:
            sampleDoublePointer = double_arr_to_ptr(sample)
            doubleOutData = <double*> out.data
            with nogil:
                self.doubleElementaryLikelihoodComputerBackend.compute_log_likelihood(
                    sampleDoublePointer, sampleSize, doubleOutData
                )
                free(sampleDoublePointer)
        
        if self.biasCorrectionFunction:
            out = self.biasCorrectionFunction(out, sample.shape[0])
            out *= self.weights
        
        return out.sum()