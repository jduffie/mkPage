from epil import *
import sys
from pageAttrs import *
from imageAttrs import *
from pageView import *
import argparse
#from __future__ import print_function
import os
from mkPage_cmn import *



# 
		
# build imageAttrs object for single image
def buildImageAttributes(srcDir, imageFilename):
    imageAttributes = imageAttrs(srcDir, imageFilename)
    return imageAttributes
	
# create a list of type imag  eAttrs
def buildImageAttributesList(srcDir):
    print indTwo + "building image list ..."
	# get a list of all images in the srcDir
	# walk the list to build the imagAttrs objects
    imageAttributesList = []
    for file in os.listdir(srcDir):  
        fileNoCase = file.upper()	
        if fileNoCase.endswith(".JPG"):
            print indThree + "processing : " + file
            imageAttributes = buildImageAttributes(srcDir, file)
            imageAttributesList.append(imageAttributes)
    return imageAttributesList


def buildPageAttributes(srcDir):
    print indTwo + "parse folder's json file ..."
    jsonFile = open(srcDir + "/folder.json")
    pageAttributes = pageAttrs(jsonFile)
    imgModel = buildImageAttributesList(srcDir)
    # TODO: append the list to the pageAttributes object
    pageAttributes.setImageModels(imgModel)
    return pageAttributes

def buildPageFiles(srcDir, pageAttributes):	
    view = pageView(pageAttributes)
    bodyHtmlStr = view.buildBody()
    with open (srcDir + "/body.html", "w") as tmpFile:
        tmpFile.write(bodyHtmlStr)	
        tmpFile.close()
    mapHtmlStr = view.buildMap()
    with open (srcDir + "/map.html", "w") as tmpFile:
        tmpFile.write(mapHtmlStr)		
        tmpFile.close()		

def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--srcDir", help="display a square of a given number")
    args = parser.parse_args()
    return args


def main(argv):
    print "mkPage - creates an html page from page descr json file and images' exif data"
    args = parseArgs(argv)
    print indOne + "Input: "
    print indTwo + "src directory: " +  args.srcDir	
    pageAttributes = buildPageAttributes(args.srcDir)
    buildPageFiles(args.srcDir, pageAttributes)
    


################
if __name__ == "__main__":
    main(sys.argv[1:])
