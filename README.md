ImageDateSort
=============


About
=====

Python script to take either single image file or a directory of images and sort by year and date stamp by extracting DateTime EXIF tag from image.


Examples
========

ImageDateSort.py

    Reads images in current dirctory and sorts to ~/Pictures/yyyy/yy.MM.dd/

ImageDateSort.py -s ~/CameraPics -d ~/MyPics -m -R -E

    Reads all images in ~/CameraPics directory and all subdirectories and outputs sorted files in ~/MyPics/yyyy/yy.MM.dd/{camera model from EXIF}/. Original files will be deleted.


Acknowledgements
================

Main function argument processing code altered from:
http://www.artima.com/weblogs/viewpost.jsp?thread=4829

    All Things Pythonic
    Python main() functions
    by Guido van van Rossum
    May 15, 2003


Extract EXIF Data function altered from:
http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/

    Posted by Mike under Python	
    Mar 28, 2010
