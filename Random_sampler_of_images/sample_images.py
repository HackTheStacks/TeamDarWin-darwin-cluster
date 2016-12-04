from numpy.random import choice
from subprocess import call

path = 'jpeacock29@darwin:/data/amnh/darwin/'
n_samples = 100

# images.txt made by,
#    ls /data/amnh/darwin/images > images.txt
# and simply lists files in images
with open('images.txt') as f:
    images = f.read().split()

# draw n_samples from images without replacement
image_samples = choice(images, n_samples, replace=False)

def run(command):
    """Runs command on the shell"""

    print('Running "{}"'.format(command))

    call(command, shell=True)

# for each sampled image, get the image file and the csvs for the north and
# south edges
for image_sample in image_samples:

    run("scp {}images/{} images".format(path, image_sample))
    run("scp {}image_csvs/{}_north.csv image_csvs".format(path, image_sample[:-4]))
    run("scp {}image_csvs/{}_south.csv image_csvs".format(path, image_sample[:-4]))
