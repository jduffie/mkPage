from epil import *
import sys
from pageAttrs import *
from imageAttrs import *
from pageView import *
import argparse
#from __future__ import print_function
import os
from mkPage_cmn import *

def buildSubDirFileList(topDir, suffix):
    print indTwo + "Searching {0} for .{1} extension".format(topDir, suffix)
    searchStr = '.' + suffix.upper()
    filesList = []
    for root, dirs, files in os.walk(topDir):
        for file in files:            
            fileNoCase = file.upper()	
            # print indThree + "fileNoCase: " + fileNoCase + "extension: " + searchStr
            if fileNoCase.endswith(searchStr):
                print indThree + "found: " + os.path.join(root, file)
                filesList.append(os.path.join(root, file))
    return filesList

def buildRouteModelsList(srcDir):
    print indTwo + "building route list ..."
	# get a list of all kml files in the srcDir
    #fileList = []
    #for file in os.listdir(srcDir):  
    #    fileNoCase = file.upper()	
    #    if fileNoCase.endswith(".KML"):
    #        fileList.append(file)
    #        print indThree + "found : " + file                    
    fileList = buildSubDirFileList(srcDir, "kml")
    return fileList
    
	
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


def buildSubPageModel(srcDir):
    subPageModel = None
    return subPageModel

def buildPageModel(srcDir):
    print indTwo + "parse folder's json file ..."
    jsonFile = open(srcDir + "/folder.json")
    pageModels = pageAttrs(jsonFile)
    imgModel = buildImageModelsList(srcDir)
    #kmlFilesList = buildKmlFileList(srcDir)
    imgCenter = findCenter(imgModel)
    routeModel = buildRouteModelsList(srcDir)
    subPageModel = buildSubPageModel(srcDir)
    # TODO: append the list to the pageModels object
    pageModels.setImageModels(imgModel)
    pageModels.setImageCenter(imgCenter)    
    pageModels.setRouteModels(routeModel)    
    pageModels.setSubPageModel(subPageModel)    
    return pageModels
    
             
def buildPageFiles(srcDir, pageModels):	
    view = pageView(pageModels)

    headMainMenuHtmlStr = view.buildHeadMainColumn()
    with open (srcDir + "/headMainColumn.html", "w") as tmpFile:    
        tmpFile.write(headMainMenuHtmlStr)	
        tmpFile.close()
    
    bodyHtmlStr = view.buildBody()
    with open (srcDir + "/body.html", "w") as tmpFile:
        tmpFile.write(bodyHtmlStr)	
        tmpFile.close()

    mapHtmlStr = view.buildMap()
    with open (srcDir + "/map.html", "w") as tmpFile:
        tmpFile.write(mapHtmlStr)		
        tmpFile.close()		
        
    sideMenuHtmlStr = view.buildSideMenu()
    with open (srcDir + "/sideMenu.html", "w") as tmpFile:
        tmpFile.write(sideMenuHtmlStr)		
        tmpFile.close()		
        
    tailMainMenuHtmlStr = view.buildTailMainColumn()
    with open (srcDir + "/tailMainColumn.html", "w") as tmpFile:    
        tmpFile.write(tailMainMenuHtmlStr)	
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
