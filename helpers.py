import pandas as pd
import numpy as np
from itertools import groupby

EUCL_NOSAMPLES = 1000


# def downsample(frame, n_chunks=100):
#     downsampled_nparray = _downsample(frame.as_matrix())
#     return pd.DataFrame(downsampled_nparray, columns=['x', 'y'])

def downsample(frame, n_chunks=100):
    n_points = frame.shape[0]
    chunk_size = int(n_points / n_chunks)  # TODO: We are throwing away any the last chunk if it doesn't fit.

    edge_frame = pd.DataFrame(frame, columns=["x", "y"])
    # downsampled = pd.DataFrame(columns=frame.columns)

    chunks = np.array(range(n_chunks))
    calc_chunk = _get_calc_chunk_mean(edge_frame, chunk_size)
    downsampled = [calc_chunk(chunk) for chunk in chunks]
    # v_calc_chunk = np.vectorize(calc_chunk)
    # downsampled = v_calc_chunk(chunks)
    return pd.DataFrame(downsampled, columns=['x', 'y'])

    # for ii in range(n_chunks):
    #     start_ii = ii * chunk_size
    #     end_ii = ii * chunk_size + chunk_size
    #     chunk_avg = edge_frame.iloc[start_ii:end_ii, :].mean()  # probs not efficient.
    #     downsampled = downsampled.append(chunk_avg, ignore_index=True)
    #     ii += 1
    # return downsampled


def _get_calc_chunk_mean(frame, chunk_size):
    def _calc_chunk_mean(chunk):
        start_ii = chunk * chunk_size
        end_ii = chunk * chunk_size + chunk_size
        means = frame.iloc[start_ii:end_ii, :].mean()
        return means.values  # probs not efficient.

    return _calc_chunk_mean


EUCL_NDPS = 3

from itertools import groupby

EUCL_NDPS = 3


def _downsample(frame, n_chunks=10 ** EUCL_NDPS):
    X = np.arange(0, 1, 1 / n_chunks)
    Y = [np.mean([i for i in g]) for k, g in groupby(frame[:, 1], (lambda x: np.round(x, EUCL_NDPS)))]
    return np.array([X, Y]).T


# def _downsample(frame, n_chunks=EUCL_NOSAMPLES):
#     n_points = frame.shape[0]
#     chunk_size = int(n_points / n_chunks)  # TODO: We are throwing away any the last chunk if it doesn't fit.
#     X = np.arange(0, 1, 1 / n_chunks)
#     i = 20
#     Y = [np.mean(frame[:, 1][np.multiply((i / n_chunks <= frame[:, 0]), (frame[:, 0] < (i + 1) / n_chunks))]) for i in
#          range(n_chunks)]
#     Y[np.isnan(Y)] = 0
#     downsampled = np.array([X, Y]).T
#     return downsampled


def axis_align(inputdata):
    # Translate leftermost point to the origin
    translateddata = inputdata - inputdata[0]

    # Find an assumed "straight edge" line:
    # straight line between first and last points
    leftpoint = translateddata[0]
    rightpoint = translateddata[-1]
    slope = (rightpoint[1] - leftpoint[1]) / (rightpoint[0] - leftpoint[0])

    # NOTE: can we get c,s more smartly?
    theta = np.arctan(slope)
    c, s = np.cos(theta), np.sin(theta)
    rotationmatrix = np.matrix('{} {}; {} {}'.format(c, -s, s, c))

    newdata = translateddata * rotationmatrix

    scalefactor = newdata[-1, 0]
    newdata[:, 0] = newdata[:, 0] / scalefactor

    return newdata


def axis_align_pandas(frame):
    return pd.DataFrame(axis_align(frame.as_matrix()), columns=frame.columns)
