from scipy import stats
import numpy as np
from numba import jit, prange

# Create a sample 1D array (replace this with your data)
#data = np.array([2, 3, 3, 4, 4, 4, 5, 5, 6, 7])
data = np.random.randint(0, 100, (10,))

# Calculate skewness
skewness = stats.skew(data)
print(skewness)

# Calculate the skewness
n = len(data)
mean = np.mean(data)
std = np.std(data, ddof=0)  # Set ddof to 0 for population standard deviation

skewness = (1/n) * np.sum(((data - mean) / std)**3)
print(skewness)



@jit('(float32[:], float64[:], int64,)')
def sliding_skew(data: np.ndarray,
                 time_windows: np.ndarray,
                 sample_rate: int) -> np.ndarray:

    """
    Compute the skewness of a 1D array within sliding time windows.

    :param np.ndarray data: Input data array.
    :param np.ndarray data: 1D array of time window durations in seconds.
    :param np.ndarray data: Sampling rate of the data in samples per second.
    :return np.ndarray: 2D array of skewness`1 values with rows corresponding to data points and columns corresponding to time windows.

    :example:
    >>> data = np.random.randint(0, 100, (10,))
    >>> skewness = sliding_skew(data=data.astype(np.float32), time_windows=np.array([1.0, 2.0]), sample_rate=2)
    """


    results = np.full((data.shape[0], time_windows.shape[0]), 0.0)
    for i in prange(time_windows.shape[0]):
        window_size = time_windows[i] * sample_rate
        for j in range(window_size, data.shape[0]+ 1):
            sample = data[j-window_size: j]
            mean, std = np.mean(sample), np.std(sample)
            results[j-1][i] = (1 / n) * np.sum(((data - mean) / std) ** 3)

    return results

@jit('(float32[:], float64[:], int64,)')
def sliding_kurtosis(data: np.ndarray,
                     time_windows: np.ndarray,
                     sample_rate: int) -> np.ndarray:
    """
    Compute the kurtosis of a 1D array within sliding time windows.

    :param np.ndarray data: Input data array.
    :param np.ndarray data: 1D array of time window durations in seconds.
    :param np.ndarray data: Sampling rate of the data in samples per second.
    :return np.ndarray: 2D array of skewness`1 values with rows corresponding to data points and columns corresponding to time windows.

    :example:
    >>> data = np.random.randint(0, 100, (10,))
    >>> kurtosis = sliding_kurtosis(data=data.astype(np.float32), time_windows=np.array([1.0, 2.0]), sample_rate=2)
    """
    results = np.full((data.shape[0], time_windows.shape[0]), 0.0)
    for i in prange(time_windows.shape[0]):
        window_size = time_windows[i] * sample_rate
        for j in range(window_size, data.shape[0] + 1):
            sample = data[j - window_size: j]
            mean, std = np.mean(sample), np.std(sample)
            results[j - 1][i] = np.mean(((data - mean) / std) ** 4) - 3
    return results







    # n = len(data)
    # mean = np.mean(data)
    # std = np.std(data)
    # skewness = (1 / n) * np.sum(((data - mean) / std) ** 3)
    # return skewness



#skewness = sliding_skew(data=data.astype(np.float32), time_windows=np.array([1.0, 2.0]), sample_rate=2)


from scipy.stats import kurtosis
import numpy as np

# Create a sample 1D array (replace this with your data)
data = np.array([2, 3, 3, 4, 4, 4, 5, 5, 6, 7])

# Calculate the kurtosis
kurtosis_value = kurtosis(data)
print(kurtosis_value)


# Calculate the kurtosis
mean = np.mean(data)
std = np.std(data, ddof=0)  # Set ddof to 0 for population standard deviation
kurtosis_value = np.mean(((data - mean) / std) ** 4) - 3
print(kurtosis_value)




