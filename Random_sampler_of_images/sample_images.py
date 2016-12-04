print("Currently doing nothing: untested code! Use with caution. Edit to run.")

from numpy.random import choice
from subprocess import call

def run(command):
    """Runs command on the shell"""

    print('Running "{}"'.format(command))

    return bool(call(command, shell=True))

path = 'jpeacock29@darwin:/data/amnh/darwin/'
n_samples = 100

def main():
    # images.txt made by,
    #    ls /data/amnh/darwin/images > images.txt
    # and simply lists files in images
    with open('images.txt') as f:
        images = f.read().split()

    # draw n_samples from images without replacement
    image_samples = choice(images, n_samples, replace=False)

    # for each sampled image, get the image file and the csvs for the north and
    # south edges. Write whether the file has associated north and south files.
    with open('samples.csv') as f:

        f.write(['image_filename', 'has_north_edge', 'has_south_edge'])

        for image_sample in image_samples:

            run("cp {}images/{} sample/images".format(path, image_sample))
            has_north_edge = run("cp {}image_csvs/{}_north.csv samples/image_csvs".format(path, image_sample[:-4]))
            has_south_edge = run("cp {}image_csvs/{}_south.csv samples/image_csvs".format(path, image_sample[:-4]))

            f.write('\t'.join([image_sample, has_north_edge, has_south_edge]) + '\n')
