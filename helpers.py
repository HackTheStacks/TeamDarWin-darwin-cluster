import pandas as pd
import numpy as np


def downsample(frame, n_chunks=100):
    n_points = frame.shape[0]
    chunk_size = int(n_points / n_chunks)  # TODO: We are throwing away any the last chunk if it doesn't fit.

    edge_frame = pd.DataFrame(frame, columns=["x", "y"])
    downsampled = pd.DataFrame(columns=frame.columns)
    ii = 0

    for ii in range(n_chunks):
        start_ii = ii * chunk_size
        end_ii = ii * chunk_size + chunk_size
        chunk_avg = edge_frame.iloc[start_ii:end_ii, :].mean()  # probs not efficient.
        downsampled = downsampled.append(chunk_avg, ignore_index=True)
        ii += 1
    return downsampled


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