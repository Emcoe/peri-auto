# peri-auto v1.1
#### Turn your favorite Periscoper into a podcast


## This was made by a beginner, be aware that everything could go wrong!

This simple utility downloads a Periscoper's user broadcasts page (e.g. https://www.periscope.tv/ABC/) and extracts the 100 recent broadcast links. It compares these to a list of links you've already seen, then downloads the new ones. These are passed to youtube-dl for downloading and conversion to 64k .m4a files with appropriate names.

The utility uses a prefs.txt file to store the Periscoper's broadcasts page URL, and the list of links to broadcasts you've already seen (peri-auto will generate a new prefs.txt if it can't find one on startup). Once you give it the target the utility runs and updates lists without any more specific input needed from you. Just run it (or schedule it!) and any new broadcasts are now audio files for you to listen to.

This was my first production Python project, and while I use it I cannot offer any guarantees or warranties for its safety or efficacy. It's a short program, so you can easily check for yourself before doing anything with it.

Requires youtube-dl, python wget, and Python 3
Created on Mac OS X 10.14 with Python 3.7
