from epil import *
import sys
from pageAttrs import *
from imageAttrs import *
from pageView import *
import argparse
#from __future__ import print_function
import os
from mkPage_cmn import *

	
# build imageAttrs object for single image
def buildImageModels(srcDir, imageFilename):
    imageModels = imageAttrs(srcDir, imageFilename)
    imageModels.resizeImages(srcDir,imageFilename)
    return imageModels
	
# create a list of type imag  eAttrs
def buildImageModelsList(srcDir):
    print indTwo + "building image list ..."
	# get a list of all images in the srcDir
	# walk the list to build the imagAttrs objects
    fileList = []

    for file in os.listdir(srcDir):  
        fileNoCase = file.upper()	
        if fileNoCase.endswith(".JPG"):
            print indThree + "found : " + file
            if fileNoCase.find("WEB.JPG") >= 0:            
                print indFour + "remove"
                os.remove(srcDir +"/" + file)
            elif fileNoCase.find("THUMB.JPG") >= 0:            
                print indFour + "remove"
                os.remove(srcDir +"/" + file)                
            else:
                print indFour + "add to list "
                fileList.append(file)
    imageModelsList = []                
    for file in fileList:  
        print indThree + "processing: " + file
        imageModels = buildImageModels(srcDir, file)
        imageModelsList.append(imageModels)
    return imageModelsList

def buildRouteModelsList(srcDir):
    print indTwo + "building route list ..."
	# get a list of all kml files in the srcDir
    fileList = []
    for file in os.listdir(srcDir):  
        fileNoCase = file.upper()	
        if fileNoCase.endswith(".KML"):
            fileList.append(file)
            print indThree + "found : " + file                    
    return fileList

def buildPageModel(srcDir):
    print indTwo + "parse folder's json file ..."
    jsonFile = open(srcDir + "/folder.json")
    pageModels = pageAttrs(jsonFile)
    imgModel = buildImageModelsList(srcDir)
    imgCenter = findCenter(imgModel)
    routeModel = buildRouteModelsList(srcDir)
    # TODO: append the list to the pageModels object
    pageModels.setImageModels(imgModel)
    pageModels.setImageCenter(imgCenter)    
    pageModels.setRouteModels(routeModel)    
    return pageModels

def buildPageFiles(srcDir, pageModels):	
    view = pageView(pageModels)

    bodyHtmlStr = view.buildBody()
    with open (srcDir + "/body.html", "w") as tmpFile:
        tmpFile.write(bodyHtmlStr)	
        tmpFile.close()

    mapHtmlStr = view.buildMap()
    with open (srcDir + "/map.html", "w") as tmpFile:
        tmpFile.write(mapHtmlStr)		
        tmpFile.close()		
        
    indexHtmlStr = view.buildIndex()
    #print "Index shtml : ", indexHtmlStr    
    with open (srcDir + "/index.shtml", "w") as tmpFile:
        tmpFile.write(indexHtmlStr)		
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
    pageModels = buildPageModel(args.srcDir)
    buildPageFiles(args.srcDir, pageModels)
    


################
if __name__ == "__main__":
    main(sys.argv[1:])
