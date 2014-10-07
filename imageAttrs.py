import json
from epil import *
from pyexif import *
from mkPage_cmn import *
from PIL import ImageOps
from math import floor
import os


class imageAttrs:

    def __init__(self, srcDir, imageFilename):
        self.data = []
        #print  indThree + imageFilename
        imgFile = srcDir + "/" + imageFilename
        self.imgFile = imageFilename
		
        try: 
            exifEditor = ExifEditor(srcDir + "/" + imageFilename)
            #print indFour + "mod time    : " , exifEditor.getModificationDateTime()
            #print indFour + "org time    : " , exifEditor.getOriginalDateTime()
            #print indFour + "description : " , exifEditor.getTag("Description")
            self.modTime = exifEditor.getModificationDateTime()
            self.descr = exifEditor.getTag("Description")

        except RuntimeError:
            print indFour + "RuntimeError: for : " + imageFilename
            self.modTime = ""
            self.descr = ""
			
        image = Image.open(imgFile)
        self.image = image
        self.exif_data = get_exif_data(image)        
        self.lat = get_lat(self.exif_data)   
        self.lon = get_lon(self.exif_data)   	
				
        print indFive + "Filename    : 	",  imageFilename		
        print indFive + "Description : 	",  self.descr		
        print indFive + "mod time    : 	", self.modTime
        print indFive + "latitude    : ", self.lat
        print indFive + "longitude   : ", self.lon

		
    def resizeImages(self, srcDir, imageFilename):
        imgFile = srcDir + "/" + imageFilename        
        
        targetWidth = 640
        targetHeight = 480              
        newImg = self.resizeImage(imgFile, targetHeight, targetWidth)
        newFilename = imageFilename.rstrip(".JPG") + "_web.JPG"
        newFilenameFull = srcDir + "/" + newFilename
        if os.path.isfile(newFilenameFull):
            print indFive +  "artifact found : remove : ", newFilenameFull
            os.remove(newFilenameFull)
        newImg.save(newFilenameFull, format='JPEG')        
        self.webFile = newFilename

        targetWidth = 128
        targetHeight = 96              
        newImg = self.resizeImage(imgFile, targetHeight, targetWidth)
        newFilename = imageFilename.rstrip(".JPG") + "_thumb.JPG"
        newFilenameFull = srcDir + "/" + newFilename
        if os.path.isfile(newFilenameFull):
            print indFive +  "artifact found : remove : ", newFilenameFull
            os.remove(newFilenameFull)
        newImg.save(newFilenameFull, format='JPEG')                
        self.thumbFile = newFilename

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

            
		
