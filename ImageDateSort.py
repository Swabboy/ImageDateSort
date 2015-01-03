# Copyright 2015 Ian Lynn 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.




from PIL import Image
from PIL.ExifTags import TAGS
from os.path import expanduser
import sys
import os
import shutil
import getopt
import fnmatch




#**********Show Error Message********** 
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
#**********Show Error Message**********

#**********Extract EXIF Data********** 
def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
#**********Extract EXIF Data********** 


#**********Parse EXIF Date Stamp********** 
def parseDateStamp(tag):

    tagDate = tag[:tag.index(" ")]
    tagYear = tagDate[:tagDate.index(":")]
    tagMonth = tagDate[tagDate.index(":")+1:tagDate.rindex(":")]
    tagDay = tagDate[tagDate.rindex(":")+1:]

    return (tagYear,tagMonth,tagDay)
#**********Parse EXIF Date Stamp********** 


#**********Get list of images********** 
def locateImages(pattern, rootDir, recur=False):
    if recur:
        for path, dirs, files in os.walk(rootDir):
            for fileName in fnmatch.filter(files, "*." + pattern):
                x = os.path.join(path, fileName)
                yield x
    else:
        fileList = os.listdir(rootDir)
        for fileName in fileList:
            if os.path.splitext(fileName)[1] == "." + pattern:
                x = os.path.join(rootDir, fileName)
                yield x

#**********Get list of images********** 


#**********Copy Image to Output Directory********** 
def SortImage(outputDir, dateTag, modelTag, imageFile, deleteOrg=False):

    #***Create directory path(Ex: ..../2014/14.12.24/CameraX)
    dateDir = os.path.join(outputDir,dateTag[0],dateTag[0][2:] + "." + dateTag[1] + "." + dateTag[2],modelTag)

    #***Create output directory if it does not exist
    try: 
        if not os.path.isdir(dateDir):
            os.makedirs(dateDir)
    except Exception, err:
        print "Unable to create output directory"
        print err
        return 0

    #***Copy the files and remove
    try:
        shutil.copy2(imageFile, dateDir)
        try:
            if deleteOrg:
                os.remove(imageFile)
        except shutil.Error, err:
            print err
    except shutil.Error, err:
        print err

#**********Check if Output Directory Exists********** 

#**********Process File**********
def ProcessFile(imageFile, modelDir=False):
    try:
        #print imageFile
        #***Get exif data
        exifData = get_exif(imageFile)
    except Exception, err:
        print "EXIF Tag does not exist for " + os.path.basename(imageFile)
        return 0

    #***Get date tag
    dateStamp = exifData["DateTime"]
    #***Parse the date tag
    parsedDateStamp = parseDateStamp(dateStamp)
                
    #***Get the camera model tag
    if modelDir:
        try:
            modelStamp = exifData["Model"]
            if modelStamp == "" or modelStamp == None:
                modelStamp = "Unknown"
        except:
            modelStamp = "Unknown"
    else:
        modelStamp=""
    return (parsedDateStamp, modelStamp)          


#**********Process File**********


#**********Show Help Text**********
def showHelp():
    f = open("HelpText.txt","r")
    try:
        helpFile = f.read()
        print helpFile
    except:
        print "Can't open help text"
    finally:
        f.close()
#**********Show Help Text**********  






#**********Main Function********** 
def main(argv=None):

    inputDir = os.curdir
    fileName = None
    delOriginal = False
    imageExt = "jpg"
    searchRecur = False
    outputDir = expanduser("~") + "/Pictures"
    numImagesProcessed = 0
    modelDir = False

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "vhf:Ex:s:d:Rm", ["help"])

 
            #***Check for help parameter
            for opt, arg in opts:
                if opt == "-h" or opt == "--help":
                    showHelp()
                    return 1

            #***Process parameters
            for opt, arg in opts:
                if opt == "-f":
		    fileName = str(arg)
                    continue
                if opt == "-E":
		    delOriginal = True
                    continue
                if opt == "-m":
		    modelDir = True
                    continue
                if opt == "-x":
                    imageExt = arg
                    continue
                if opt == "-s":
                    inputDir = os.path.abspath(arg)
                    continue
                if opt == "-d":
                    outputDir = os.path.abspath(arg)
                    try:
                        if not os.path.isdir(dateDir):
                            os.makedirs(dateDir)
                    except:
                        print "Unable to create output directory: " + outputDir
                        return 2
                    continue
                if opt == "-R":
                    searchRecur = True
                    continue

            #***Get list of images
            if fileName == None:   
                print "Finding Images"
 
                imageList = locateImages(imageExt, os.path.abspath(inputDir), searchRecur)

                print "Processing Images"

                for imageFile in imageList:
                    exifData = ProcessFile(imageFile,modelDir)
                    if exifData == 0:
                        continue

                    #***Sort the images into their respective directories
                    SortImage(outputDir,exifData[0],exifData[1],imageFile,delOriginal)
                    numImagesProcessed += 1

                #***Complete***
                print "Finished"
                print "Number of images processed: " + str(numImagesProcessed)

            else:
                 print "Processing Image"
                 exifData = ProcessFile(fileName,modelDir)
                 
                 if exifData == 0:
                     print "No EXIF data found to sort image"
                 else:
                     SortImage(outputDir,exifData[0],exifData[1],fileName,delOriginal)
                     print "Finished"

        except getopt.error, msg:
             raise Usage(msg)

	    
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use -h or --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
#**********Main Function********** 



