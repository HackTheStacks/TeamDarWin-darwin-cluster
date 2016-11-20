import pandas as pd


def downsample(frame, chunk_size=5):
    n_points = frame.shape[0]
    n_chunks = int(n_points / chunk_size)  # TODO: We are throwing away any the last chunk if it doesn't fit.

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
