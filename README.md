# SpatialTemporalImage-CMPT365

## General info
This is the submission of the final project for CMPT-365, and we call it TRANSformer. This software can
tell what video transitions occur and at what time. 
But we don't stop there, because that was too easy. The software now visually tells you where the transition
is in the video itself. It highlights the transition in the video itself. Try it out for yourself.

## Libraries
We used:
* python v3.8
* setuptools v40.8.0
* numpy v1.18.1
* openCV-python v4.2.0.32
* matplotlib v3.2.0
## To run
```buildoutcfg
$ cd [directory]
$ python setup.py install
$ TRANSformer [flags] [valid video file path]
```
#### Flags
* *-h*:  sends help. Exactly what I am doing here, just with more detail.
* *-v*: enables verbose mode
* *-o*: outputs the enhanced video and STIs to the directory directly followed.
* *-rg*: Forces the code program to regenerate the STI even if it already exists. Without this, the program
may skip STI generation if it finds a file with the same name as the video followed by _rowsti/_colsti.
* *-w*: writes the STI to the directory for faster video enhancement next time.
* *-s*: lets you decide the resizing. Keep it small for faster processing. Not too small.
* *-r*: lets you decide the video resolution.
* *-t*: lets you pick the threshold value for our HoughLine filter for line detection. Default is 40.
* *-i*: enables the IBM algorithm instead.
* *-c*: lets you customize the palette of colors for our transitions in videos. you can choose between *pastel*
*, vibrant, neon, grey, lyl.*

