import os
import numpy as np

EUCL_NOSAMPLES = 1000
SMOOTHING_FACTOR = 30

def downsample(frame, n_chunks=EUCL_NOSAMPLES):
    n_points = frame.shape[0]
    chunk_size = int(n_points / n_chunks)  # TODO: We are throwing away any the last chunk if it doesn't fit.
    X = np.arange(0,1,1/n_chunks)
    i=20
    Y = [np.mean(frame[:,1][np.multiply((i/n_chunks <= frame[:,0]),(frame[:,0] < (i+1)/n_chunks))]) for i in range(n_chunks)]
    downsampled = np.array([X,Y]).T
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
    
    newdata =  translateddata * rotationmatrix
    scalefactor = newdata[-1,0]
    newdata[:,0] = newdata[:,0] / scalefactor
    
    return newdata

def get_aligneddata(filename):
    inputcsv = np.genfromtxt(filename, delimiter=',')
    inputcsv = inputcsv[1:,(1,2)]
    inputcsv.sort(0)
    aligned_data = axis_align(inputcsv)
    return aligned_data

def main_fn(csv_folder_loc):
	yvalues = []
	for csvfile in os.listdir(csv_folder_loc):
	    name = os.abspath(csvfile)
	    y = get_aligneddata(name)
	    y = downsample(y)
	    y[np.isnan(y)] = 0
	    yvalues.append(np.array(y[:,1]))
	yvalues.append(np.zeros(1000))
	return yvalues



