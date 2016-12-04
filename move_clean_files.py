import os
from shutil import copyfile
import pdb
import sys

clean_list = sys.arg[1]
source_dir = sys.arg[2]
clean_dir = sys.arg[3]

'''
for example:
source_dir = './image_csvs_fft'
clean_dir = './image_csvs_fft_clean'
clean_list = 'images_clean.txt'
'''

with open(clean_list) as f:
  clean_files = [i.strip("\n") for i in f.readlines()]

clean_files = {i:i.split(".")[0] for i in clean_files}
source_files = {i:i.split("_")[0] for i in os.listdir(source_dir)}

for source_filename, source_filemark in source_files.items():
  for clean_filename, clean_filemark in clean_files.items():
    if source_filemark == clean_filemark:
      print("Match {},{}".format(source_filename,clean_filename), end=" ")
      source_path = os.path.join(source_dir,source_filename)
      clean_path = os.path.join(clean_dir,source_filename)
      copyfile(source_path,clean_path)
      break
