Sample generation
=================
Select a random sample of 100 of the 35k image files and download them. Assumes "images" and "image_csvs" directories.

The current (3:45p December 4th, 2016) /data/amnh/darwin/samples folder was created by running "sample_images.py" on a different machine and scp the results to the server. Subsequent modifications have not been tested, but should make the script runnable on the server and keep a log of which images and csvs were found.

Sample labeling
===============
A csv file, named "labeled_samples.csv" includes the following columns:

filename: (string) Name of image file
has_north_edge: ("True"|"False") of whether the filename has an associated _north.csv file
has_south_edge: ("True"|"False") of whether the filename has an associated _south.csv file
north_type: ("fuzzy"|"straight"|"curvy"|"na") Whether the edge appears fuzzy, straight, curvy or there is no applicable classification
south_type: ("fuzzy"|"straight"|"curvy"|"na")
fullpage: ("1"|"0") Whether the page appears to be a full page and therefore no matching edge
text: (0|0.5|1) 0 if the page is blank, 0.5 if there is some text on the page, 1 if the page is full of text
notes: (string) Interesting notes about the file
color: ('na'|'blue'|'yellow'|empty) The rough color of the paper
