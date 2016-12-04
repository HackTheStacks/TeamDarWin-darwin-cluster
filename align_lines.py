from tqdm import tqdm
import os
import numpy as np
import sys
from sklearn.metrics.pairwise import euclidean_distances
import json
from itertools import groupby

SMOOTHING_FACTOR = 30
EUCL_NDPS = 3

def downsample(frame, n_chunks=10**EUCL_NDPS):
    meansdict = {np.round(k,EUCL_NDPS):np.mean([i[0,1] for i in g])
                for k,g in
                groupby(frame, (lambda x: np.round(x[0,0], EUCL_NDPS)))}
    Y = np.zeros(1000)
    for key in meansdict:
        Y[key*1000-1] = meansdict[key]

    return Y

def axis_align(rawcsv:np.array):
    """Inputs: rawcsv: a numpy array containing numerical csv data

    Outputs: 1d numpy array containing normalised points:
            - rotated to the x-axis
            - scaled to [0,1] horizontal (optional)
            - TODO: vertical scaling?
    """
    # Translate leftermost point to the origin
    translateddata = rawcsv - rawcsv[0]

    # Find an assumed "straight edge" line:
    # straight line between first and last points
    leftpoint = translateddata[0]
    rightpoint = translateddata[-1]
    slope = (rightpoint[1] - leftpoint[1]) / (rightpoint[0] - leftpoint[0])
    # NOTE: can we get c,s more smartly?
    theta = np.arctan(slope)
    c, s = np.cos(theta), np.sin(theta)
    rotationmatrix = np.matrix('{} {}; {} {}'.format(c, -s, s, c))

    newdata =  translateddata * rotationmatrix
    scalefactor = newdata[-1,0]
    newdata[:,0] = newdata[:,0] / scalefactor

    return newdata

def get_aligned_data(filename):
    """Takes a filename containing raw edge data in csv format
    Runs the "axis_align" function
    Returns a numpy array containing normalised edge data
    """
    inputcsv = np.genfromtxt(filename, delimiter=',')
    inputcsv.sort(0)
    aligned_data = axis_align(inputcsv)
    return aligned_data

def filter_zero_files(csv_folder_loc):
    """"""
    tqdm(os.listdir(csv_folder_loc))
    return os.path.getsize(os.path.join(csv_folder_loc,csvfile)) > 0:

def get_aligned_lines(csv_folder_loc):
    yvalues = []
    filenames = []

    """Read files from the given folder"""
    for csvfile in tqdm(os.listdir(csv_folder_loc)):
        if os.path.getsize(os.path.join(csv_folder_loc,csvfile)) > 0:
            name = os.path.join(csv_folder_loc,csvfile)

            """For each file, call get_aligned_data to process the data
            contained in the file."""
            y = get_aligned_data(name)
            y = downsample(y)
            y[np.isnan(y)] = 0
            yvalues.append(np.array(y))
            filenames.append(csvfile)
    #TODO: zero value append add it back when we have k-means
    #yvalues.append(np.zeros(1000))
    stacked_lines = np.vstack(yvalues)
    return stacked_lines,filenames

def get_distances(stacked_lines,filenames,num_matches=10):
    closest_friends=[]
    dist_matrix = euclidean_distances(stacked_lines)
    for i,filename in zip(dist_matrix,filenames):
        zipped = list(zip(i,filenames))
        zipped.sort(key=lambda tup: tup[0])
        top_matches = zipped[1:num_matches+1]
        top_matches = [z[1] for z in top_matches]
        closest_friends.append((filename,top_matches))
    return closest_friends

def save_to_json(closest_friends,save_path):
    with open(save_path, 'w') as outfile:
        json.dump(closest_friends, outfile)

if __name__ == "__main__":
    stacked_lines,filenames = get_aligned_lines(sys.argv[1])
    closest_friends = get_distances(stacked_lines,filenames,num_matches=10)
    save_to_json(closest_friends, sys.argv[2])
