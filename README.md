# Evolution of Darwin's Notes Reconstruction

This repo contains the machine learning functions for the [AMNH Hack the Stacks](http://www.amnh.org/learn-teach/adults/bridgeup-stem/hackathon) challenge by team DarWin. The challenge was to create a project to piece together Charles Darwin's notes, which he often would cut up and reorganize by topic, e.g.:

>Darwin was in the habit of frequently reorganizing his notes according to the topics that particularly interested him at a given time. This meant, for example, that a page of observations made in 1840 on bees visiting flowers might, in 1850, have been torn apart or cut up into two pieces and each piece put into a separate topical portfolio. One portfolio could be devoted to the behavior of bees and the other to the anatomy of flowers. In an age of only literal cutting and pasting, this was an important way for Darwin to shuffle and organize his thoughts and his observations.

The overall project won *Most Original Hack* during the competition. A link to the challenge description can be found [here](https://github.com/amnh/HackTheStacks/wiki/The-Evolution-of-Darwin's-Notes).

## Overview

+ The main function *align_lines.py* takes as an input a path to a folder of .csv files containing path vectors for note edges and returns a matrix of the file corresponding to each edge and it's closest 10 neighboring edges as a JSON file. 
+ The path vectors were extracted from images of Darwin's note edges using [these computer vision scripts](https://github.com/HackTheStacks/darwin-notes-image-processing). 
+ The JSON file is then fed into the [Darwin Viewer API](https://github.com/HackTheStacks/darwin-viewer) which can be visualized using the [Darwin Viewer Mobile App](https://github.com/HackTheStacks/darwin-viewer-mobile).
