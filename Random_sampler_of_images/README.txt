
Sample generation
=================
Select a random sample of 100 of the 35k image files and download them. Assumes "images" and "image_csvs" directories.

The current (3:45p December 4th, 2016) /data/amnh/darwin/samples folder was created by running "sample_images.py" as of commit ### on a different machine and scp the results to the server. Subsequent modifications have not been tested, but should make the script runnable on the server and keep a log of which images and csvs were found.


Sample labeling
===============
After generating the sample of 100 images, they were hand-rated with the following information:

- Validate ruler consistency and scaling outputs
- Color
- Which edges are which shapes/types
- Cases degenerate edges
- Do front/back pairs consistently have blank backs?
- How much text is included?
