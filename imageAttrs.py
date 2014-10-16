import json
import exiftool
from epil import *
#from pyexif import *
from mkPage_cmn import *
#from PIL import ImageOps
from math import floor
import os


def dumpMetadata(imgFiles):
    if imgFiles:
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata_batch(imgFiles)
    cnt = 0
    for d in metadata:
        filePtr = open(imgFiles[cnt]+".json", 'w')
        json.dump(d, filePtr, indent=4)
        cnt = cnt + 1

class imageAttrs:

    def __init__(self, srcDir, md):
        self.data = []

        self.srcDir = srcDir
        self.md = md

        # this is the only way I can extract description
        self.descr = ""
        self.lat = ""
        self.lon = ""
        self.modTime = ""
        gpsLat = None
        gpsLon = None
        gpsLatRef = None
        gpsLonRef = None
        for elem in md:
            if elem == 'XMP:Description':
                self.descr = md[elem]
            if elem == 'EXIF:GPSLatitude':
                gpsLat = md[elem]
            if elem == 'EXIF:GPSLatitudeRef':
                gpsLatRef  = md[elem]
            if elem == 'EXIF:GPSLongitude':
                gpsLon = md[elem]
            if elem == 'EXIF:GPSLongitudeRef':
                gpsLonRef = md[elem]
            if elem == 'EXIF:DateTimeOriginal':
                self.modTime = md[elem]
            if elem == 'File:FileName':
                self.imgFile = md[elem]

        if gpsLat and gpsLatRef :
            lat = gpsLat
            if gpsLatRef  != "N":
                lat = 0 - lat
            self.lat = lat

        if gpsLon and gpsLonRef :
            lon = gpsLon
            if gpsLonRef  != "E":
                lon = 0 - lon
            self.lon = lon


        print indFive + "Filename    : 	", self.imgFile
        print indFive + "Description : 	", self.descr
        print indFive + "mod time    : 	", self.modTime
        print indFive + "latitude    :  ", self.lat
        print indFive + "longitude   :  ", self.lon

		
    def resizeImages(self):
        srcDir = self.srcDir
        imageFilename = self.imgFile
        imageFilenameFull = srcDir + "/" + imageFilename


        newFilename = imageFilename.rstrip(".JPG") + "_web.JPG"
        newFilenameFull = srcDir + "/" + newFilename
        targetWidth = 640
        targetHeight = 480
        self.resizeImageStart(imageFilenameFull, newFilenameFull, targetWidth, targetHeight)
        self.webFile = newFilename

        newFilename = imageFilename.rstrip(".JPG") + "_thumb.JPG"
        newFilenameFull = srcDir + "/" + newFilename
        targetWidth = 128
        targetHeight = 96
        self.resizeImageStart(imageFilenameFull, newFilenameFull, targetWidth, targetHeight)
        self.thumbFile = newFilename


    def resizeImageStart(self, imageFilenameFull, newFilenameFull, targetWidth, targetHeight):

        create = False
        #print indFive +  "testing : ", newFilenameFull
        if os.path.isfile(newFilenameFull):
            #print indSix  +  "artifact found : ", newFilenameFull
            if os.path.getctime(newFilenameFull) < os.path.getctime(imageFilenameFull) :
                #print indSix + "older, rebuild: " +  newFilenameFull
                create = True
        else :
            #print indSix  + "not found: " +  newFilenameFull
            create = True
        if create:
            #print indSix  + "create: " +  newFilenameFull
            newImg = self.resizeImage(imageFilenameFull, targetHeight, targetWidth)
            newImg.save(newFilenameFull, format='JPEG')
        #else :
            #print indSix  + "preserve: " +  newFilenameFull


    def resizeImage(self, imgFile, targetHeight, targetWidth):
        img = Image.open(imgFile)
        width, height = img.size
        #print "width,height: ", width,height
        dstWidth = width
        dstHeight = height

        if dstWidth > targetWidth:
            ratio = float(targetWidth)/float(dstWidth)
            dstWidth = targetWidth
            dstHeight = int(ratio * dstHeight)

        if dstHeight > targetHeight:
            ratio = float(targetHeight)/float(dstHeight)
            dstHeight = targetHeight
            dstWidth = int(ratio * dstWidth)

        newImg = img.resize((dstWidth, dstHeight), Image.ANTIALIAS)
        return newImg
            
		
