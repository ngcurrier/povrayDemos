$!/bin/bash
rm -f planets.mp4
povray planets.ini
ffmpeg -r 30 -f image2 -s 1920x1080 -i planets%03d.png -vcodec libx264 -crf 15 -pix_fmt yuv420p planets.mp4
