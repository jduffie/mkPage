import json
import exiftool
from epil import *
#from pyexif import *
from mkPage_cmn import *
#from PIL import ImageOps
from math import floor
import os
from imageAttrs import *
import pprint


class imageSet:

    def __init__(self, srcDir, imageFileList):
        self.data = []
        self.srcDir = srcDir
        self.imageFileList = imageFileList

    def buildImageModelListMd(self):
        self.mdList = []
        if self.imageFileList:
            with exiftool.ExifTool() as et:
                self.mdList = et.get_metadata_batch(self.imageFileList)

        imageModelList = []
        for md in self.mdList :
            imageModel = imageAttrs(self.srcDir, md)
            imageModelList.append(imageModel)
        self.imageModelList = imageModelList

    def writeMdToJson(self):
        cnt = 0
        for md in self.mdList :
            filePtr = open(md["SourceFile"]+".json", 'w')
            json.dump(md, filePtr, indent=4)
            cnt = cnt + 1

    def findCenter(self):
        avgLat = 0
        avgLon = 0
        sumLat = 0
        sumLon = 0
        cnt = 0
        for imageModel in self.imageModelList:
            if imageModel.lat and imageModel.lon:
                sumLat = sumLat + imageModel.lat
                sumLon = sumLon + imageModel.lon
                cnt = cnt + 1

        if cnt > 0:
            avgLat = sumLat / cnt
            avgLon = sumLon / cnt

        #print indThree + "Avg Lon : ", avgLon
        #print indThree + "Avg Lat : ", avgLat
        return avgLat,avgLon

