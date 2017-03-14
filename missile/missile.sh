#!/bin/bash
rm -f missile.mp4
povray missile.ini 
ffmpeg -r 10 -f image2 -s 1920x1080 -i missile%02d.png -vcodec libx264 -crf 15 -pix_fmt yuv420p missile.mp4
