from tqdm import tqdm
import os
import numpy as np
import sys
from sklearn.metrics.pairwise import euclidean_distances
import json
from itertools import groupby

SMOOTHING_FACTOR = 30
#downsample will sample the input to 10^NO_DECIMAL_PLACES x-values.
NO_DECIMAL_PLACES = 3

def downsample(inputarray, resolution=NO_DECIMAL_PLACES):
    """Input: a 2d numpy array of x,y values, with x in [0,1]
    > Maps each x-value to its nearest 10^(-NO_DECIMAL_PLACES) value (the new x-values)
    > Takes the mean of each of these groups, to get a new y-value for each new x-value
    Puts the new y-values into a length 10^NO_DECIMAL_PLACES vector
    Output: a 10^NO_DECIMAL_PLACES array of normalised values."""

    def rounded_y_value(point):
        return np.round(point[0,0], NO_DECIMAL_PLACES)

    if max(inputarray[0,:]) > 1 or min(inputarray[0,:]) < 0:
        print("Image not normalised to [0,1] in the x-axis")

    points_grouped_by_nearest_xval = groupby(inputarray, rounded_y_value)
    mean_yvalues = [np.mean(ys) for x,ys in points_grouped_by_nearest_xval]
    return np.array(mean_yvalues)

    """Y = np.zeros(10**NO_DECIMAL_PLACES)
    Y = np.array(meansdict.values())
    for key in meansdict:
        Y[key*10**NO_DECIMAL_PLACES - 1] = meansdict[key]

    return Y"""

def axis_align(rawcsv:np.array):
    print(rawcsv)
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
    print(leftpoint, rightpoint)
    slope = (rightpoint[1] - leftpoint[1]) / (rightpoint[0] - leftpoint[0])
    # NOTE: can we get c,s more smartly?
    theta = np.arctan(slope)
    c, s = np.cos(theta), np.sin(theta)
    print(theta, c, s)
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
    """Filters the zero-sized files from csv_folder_loc,
    returns a list of good files."""

    def filesize(filename):
        return os.path.getsize(os.path.join(csv_folder_loc,filename))

    listoffiles = os.listdir(csv_folder_loc)
    return [file for file in listoffiles if filesize(file) > 0]

def get_aligned_lines(csv_folder_loc):
    yvalues = []
    filenames = []

    """Read files from the given folder"""
    for csvfile in filter_zero_files(csv_folder_loc):
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
    get_aligned_data("./sample_csv/77726_MS-DAR-00205-00001-000-00096_south.csv")
    """stacked_lines,filenames = get_aligned_lines(sys.argv[1])
    closest_friends = get_distances(stacked_lines,filenames,num_matches=10)
    save_to_json(closest_friends, sys.argv[2])"""
