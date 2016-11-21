# Darwin Notes Reconstruction

This repo contains the machine learning functions for the AMNH Hack the Stacks challenge by team DarWin.

## Overview

The main function *align_lines.py* takes as an input a path to a folder of .csv files containing path vectors for note edges and returns a matrix of each edge and it's closest 10 neighboring edges as a JSON file. The path vectors were extracted from images of Darwin's note edges using [these computer vision scripts](https://github.com/HackTheStacks/darwin-notes-image-processing). The JSON file is then fed into the [Darwin Viewer API](https://github.com/HackTheStacks/darwin-viewer) which can be visualized using the [Darwin Viewer Mobile App](https://github.com/HackTheStacks/darwin-viewer-mobile).
