from epil import *
import sys
from pageAttrs import *
from imageSet import *
from imageAttrs import *
from pageView import *
import argparse
#from __future__ import print_function
import os
from mkPage_cmn import *

# if file has spaces, dashes, etc move to new name
def saneFile(srcDir, srcFilename):
    dstFilename = srcFilename
    dstFilename = dstFilename.replace("-", "_")
    dstFilename = dstFilename.replace(" ", "_")
    dstFilename = dstFilename.replace(".jpg", ".JPG")
    dstFilename = dstFilename.replace(".jpeg", ".JPG")
    dstFilename = dstFilename.replace(".JPEG", ".JPG")
    dstFilename = dstFilename.replace(".KML", ".kml")
    if srcFilename != dstFilename:
        oldName = srcDir + '/' + srcFilename
        newName = srcDir + '/' + dstFilename
        os.rename(oldName, newName)
    return dstFilename

# recursively search subdirs for instances of a file with given suffix 
def buildAllSubDirFileList(topDir, suffix):
    print indTwo + "Searching {0} for .{1} extension".format(topDir, suffix)
    searchStr = "." + suffix.upper()
    filesList = []
    for root, dirs, files in os.walk(topDir):
        for file in files:            
            fileNoCase = file.upper()	
            #print indThree + "file : " + file
            if fileNoCase.endswith(searchStr):
                print indThree + "found: ", os.path.join(root, file)
                filesList.append(os.path.join(root, file))
    return filesList

# search all immediate subdirs for instances of a file with given filename
def buildSubDirFileList(topDir, fileName):
    print indTwo + "Searching {0} for .{1} extension".format(topDir, fileName)
    filesList = []
    for dir in os.walk(topDir).next()[1]:
        testFile = dir + "/" + fileName
        if os.path.isfile(testFile):
            filesList.append(testFile)
    return filesList

def buildNestedFoldersMdList(srcDir):
    print indTwo + "building list for folder meta data for nested folders ..."
    fileList = []    
    jsonFileList = buildSubDirFileList(srcDir, "folder.json")
    for file in jsonFileList:
        if "folder.json" in file :
            print indThree + "adding mdFile : ", file
            fileList.append(file)
    return fileList

def buildSubPageModel(srcDir):
    subPageModelList = []
    mdFileList = buildSubDirFileList(srcDir, "folder.json")
    for mdFile in mdFileList:
        pageModel =  pageAttrs(mdFile)
        subPageModelList.append(pageModel)
        print indTwo + "appending : ", pageModel.title
    return subPageModelList

def buildParentPageModel(srcDir):
    testFile = srcDir + "/../folder.json"
    pageModel = None
    if os.path.isfile(testFile):
        print indTwo + "adding parent mdFile : ", testFile
        pageModel =  pageAttrs(testFile)
    return pageModel
    
    
# build imageAttrs object for single image
def buildImageModels(srcDir, imageFilename):
    imageModels = imageAttrs(srcDir, imageFilename)
    imageModels.resizeImages(srcDir,imageFilename)
    return imageModels

# create a list of type imag  eAttrs
def buildImageModelList(srcDir):
    print indTwo + "building image list ..."
        # get a list of all images in the srcDir
        # walk the list to build the imagAttrs objects
    fileList = []

    for file in os.listdir(srcDir):
        fileNoCase = file.upper()
        if fileNoCase.endswith(".JPG"):
            print indThree + "found : " + file
            if "WEB.JPG" in fileNoCase:
                continue
            if "THUMB.JPG" in fileNoCase:
                continue
            else:
                print indFour + "add to list "
                file = saneFile(srcDir, file)
                fileList.append(srcDir + "/" + file)

    print indTwo + "image list ...", fileList
    imSet = imageSet(srcDir, fileList)
    imSet.buildImageModelListMd()
    imSet.writeMdToJson()

    for model in imSet.imageModelList:
        model.resizeImages()

    print imSet
    for im in imSet.imageModelList:
        print im
    return imSet


def buildRouteModelsList(srcDir):
    print indTwo + "building route list ..."
    fileList = buildAllSubDirFileList(srcDir, "kml")
    return fileList


def buildPageModel(srcDir):
    print indTwo + "parse folder's json file ..."
    jsonFileName = srcDir + "/folder.json"
    pageModels = pageAttrs(jsonFileName)

    imSet = buildImageModelList(srcDir)
    for im in imSet.imageModelList:
        print im

    pageModels.setImageModels(imSet.imageModelList)

    imgCenter = imSet.findCenter()
    pageModels.setImageCenter(imgCenter)

    routeModel = buildRouteModelsList(srcDir)
    pageModels.setRouteModels(routeModel)

    subPageModel = buildSubPageModel(srcDir)
    pageModels.setSubPageModel(subPageModel)

    parentPageModel = buildParentPageModel(srcDir)
    pageModels.setParentPageModel(parentPageModel)

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
