# KDE-Likelihood

A python package to compute kernel-density-estimated likelihood.

## Installation

To compile and use this package, you need python 3 and pip. 

You can install this package by typing 

```
pip install kdelikelihood
```

If you are using a platform or python version for which no precompiled binaries are available, you need a c++ compiler. On Linux, the compiler should not be a concern; on Windows, you need the Visual Studio 2019 compiler, which you may get by downlaoding and installing the [Buildtools for Visual Studio](https://visualstudio.microsoft.com/de/vs/older-downloads/). 

To build this package from source, proceed as follows. If you have python and pip installed and available on the `PATH`, navigate to the project folder in which you find `setup.py`. Execute

```
pip install .
```



## Usage example:

```python

import numpy as np
from kdelikelihood import ParallelLikelihoodComputer, get_bandwidth_by_silverman, plot_smoothened


# Some model for simulating the data
def model(parameters, sampleSize=10000):
    result = np.zeros((sampleSize, 3))

    # Suppose the first column contains some count data
    result[:, 0] = np.random.poisson(parameters[0], size=sampleSize)

    # Suppose the second column contains some positive data
    result[:, 1] = np.random.randn(sampleSize) ** 2 * parameters[1] + result[:, 0]

    # Suppose the third column contains some unconstrained data
    result[:, 2] = np.random.randn(sampleSize) * result[:, 1] * parameters[2]

    return result


# The observed data (each row is an independent sample)
observedData = np.array(
    [
        [1.0, 1.11921911, -0.71177555],
        [6.0, 6.02855478, 8.37566854],
        [3.0, 9.57724975, 6.41826056],
        [5.0, 5.64429256, 6.24338937],
        [8.0, 9.57156202, 7.87944723],
        [4.0, 4.84531121, -0.65146309],
        [7.0, 7.03391557, -8.34715355],
        [3.0, 3.04287902, 0.92252008],
        [7.0, 7.00074299, 0.98825773],
        [5.0, 5.83488089, -6.66077578],
        [6.0, 6.26802035, -6.32007646],
        [4.0, 4.00099543, -5.72002288],
        [2.0, 2.61069588, 1.98710941],
        [7.0, 8.08870818, -11.84123493],
        [4.0, 4.20187965, 2.96009114],
        [2.0, 3.21568321, -0.51097464],
        [3.0, 9.08856868, 10.7647393],
        [5.0, 5.00020691, -4.58271643],
        [5.0, 11.4222031, 5.95202002],
        [5.0, 5.64400458, -4.22623137],
        [6.0, 7.08425759, -3.3731975],
        [4.0, 4.59795136, -4.37783711],
        [4.0, 7.20161146, -3.36315821],
        [3.0, 3.00051945, -2.39977869],
        [1.0, 3.05606476, -1.18190334],
        [2.0, 2.18191751, 2.29985054],
        [5.0, 5.11884191, -0.74355017],
        [5.0, 5.92561278, -8.76376851],
        [2.0, 4.19454749, 13.87107752],
        [5.0, 5.00930303, -0.34471651],
    ]
)

# The type of data we are considering in each column:
# 0: unconstrained real numbers
# 1: non-negative real numbers
# 2: natural numbers
modes = [2, 1, 0]

# The size of the sample we are generating for each parameter set
# to estimate the likelihood
sampleSize = 10000

# Bandwidths. Smaller values mean reduced bias if the sample is large enough.
# Bigger values mean reduced stochasticity of the result.
# As a start, we could use the rule of thumb of Silverman
bandwidths = get_bandwidth_by_silverman(observedData, sampleSize)

# Tolerance for the result
# This is not really a rigorous quantity. Bigger values make
# computations faster; smaller values increase the accuracy
atol = 1e-10

# To avoid the "curse of dimensionality", we can consider parts of the data
# as independent. However, since the data are interdependent in our example,
# we say they all belong to the same group. That is, we have one group only.
dataGroups = 1

# Note: if we considered a model returning many (>5) data columns, we might consider some
# of them independent of one another to reduce the stochasticity of the
# likelihood estimate. If the model parameters do not primarily control the dependency,
# then the parameter estimates will still converge to the correct values.

# Set up a likelihood computer based on the observed data
with ParallelLikelihoodComputer(observedData, bandwidths, modes, dataGroups, atol) as cmp:
    # Some parameters:
    # (here, this are the true parameters used to generate the data set, but
    #  in practice, we would not know of course)
    parameters = [5, 1, 1]

    # Get some data set from a simulation (each row is a "quasi-independent" sample)
    simulatedData = model(parameters, sampleSize)

    # Compute the likelihood
    logLikelihood = cmp.compute_log_likelihood(simulatedData)

    print("Ln(Likelihood):", logLikelihood)

    # To optimize this, we could use the suggested workflow implemented in the package,
    # which uses the package py-bobyqa (https://github.com/numericalalgorithmsgroup/pybobyqa/)
    from kdelikelihood import maximize_log_likelihood

    # Define the objective function
    def log_likelihood(parameters):
        # Generate a sample from the model
        sample = model(parameters, sampleSize)

        # Return the log-likelihood
        return cmp.compute_log_likelihood(sample)

    # Define some bounds for the parameters
    bounds = [(1e-10, 20), (0, 20), (0, 20)]

    # Maximize the likelihood
    result = maximize_log_likelihood(log_likelihood, bounds)

    # Print the result
    print(result)

    # For comparison, the likelihood estimated based on the true parameters:
    print("Likelihood of the original parameters:", log_likelihood(parameters))

    # Now we check the marginal distribution of the results and see 
    # if the heuristic bandwidth choice was appropriate 
    from matplotlib import pyplot as plt
    
    fig, axes = plt.subplots(figsize=(10, 4), ncols=observedData.shape[1])
    axes[0].set_ylabel("Density")
    for i, axis in enumerate(axes):
        plot_smoothened(model(result.x, sampleSize)[:,i], bandwidth=bandwidths[i], label="Model", axis=axis)
        plot_smoothened(observedData[:,i], onlyHistogram=True, label="Data", axis=axis)
        axis.set_xlabel("Feature {}".format(i+1))
    
    axis.legend()
    plt.tight_layout()
    plt.show()
    
    # We see that the smoothed curve does not fit the histogram for the fitted
    # model very well. Hence, we decrease the bandwidths
    
    bandwidths[0] *= 0.5
    bandwidths[1] *= 0.05
    bandwidths[2] *= 0.2
    
    # Now we repeat the fitting procedure
    
    # Maximize the likelihood
    result = maximize_log_likelihood(log_likelihood, bounds)

    # Print the result
    print(result)

    # The resulting parameters are closer to the real ones 
    # and also the cueves overlap better. This would be
    # visible more strongly if we used a larger dataset 
    # as basis for our model fit.
    fig, axes = plt.subplots(figsize=(10, 4), ncols=observedData.shape[1])
    axes[0].set_ylabel("Density")
    for i, axis in enumerate(axes):
        plot_smoothened(model(result.x, sampleSize)[:,i], bandwidth=bandwidths[i], label="Model", axis=axis)
        plot_smoothened(observedData[:,i], onlyHistogram=True, label="Data", axis=axis)
        axis.set_xlabel("Feature {}".format(i+1))
    
    axis.legend()
    plt.tight_layout()
    plt.show()
    

```
