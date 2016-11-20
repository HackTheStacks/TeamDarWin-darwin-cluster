import pandas as pd
import os
import helpers
from sklearn.cluster import KMeans

FEAT_TRANSFORM = {
    'Points:0': 'x',
    'Points:1': 'y'
}

DATA_DIR = 'sample_csv'
OUT_FILE = './clusters.csv'

N_CLUSTERS = 5


def cluster_edges(input_dir, output_file):
    file_names = os.listdir(input_dir)

    edges = []
    for file_name in file_names:
        edge = helpers.axis_align_pandas(load_edge(file_name).sort_values(by='x'))
        edges.append(edge)

    downsampled_edges = []
    for edge in edges:
        downsampled_edges.append(helpers.downsample(helpers.axis_align_pandas(edge), 1000))

    total_frame_cols = get_cols_from_frame(downsampled_edges[0])
    total_frame = pd.DataFrame(columns=total_frame_cols)

    for edge in downsampled_edges:
        total_frame = total_frame.append(frame_to_row(edge), ignore_index=True)

    kmeans = KMeans(N_CLUSTERS)
    kmeans.fit(total_frame)
    clusters = kmeans.predict(total_frame)
    pd.DataFrame({
        'filename': file_names,
        'cluster': clusters
    }).to_csv(output_file, index=False)


def load_edge(file_name):
    image_path = '%s/%s' % (DATA_DIR, file_name)
    return pd.read_csv(image_path)[list(FEAT_TRANSFORM.keys())].rename(columns=FEAT_TRANSFORM)


def frame_to_row(in_frame):
    cols = get_cols_from_frame(in_frame)
    unstacked = in_frame.unstack()
    return pd.Series(unstacked.ravel(), index=cols)


def get_cols_from_frame(in_frame):
    unstacked = in_frame.unstack()
    return list('y' + unstacked['y'].index.astype(str)) + list('x' + unstacked['x'].index.astype(str))


if __name__ == '__main__':
    input_dir = './%s' % DATA_DIR
    cluster_edges(input_dir, OUT_FILE)
