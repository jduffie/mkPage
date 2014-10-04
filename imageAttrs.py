import json
from epil import *
from pyexif import *
from mkPage_cmn import *


#indOne = "    "
#indTwo = indOne + indOne
#indThree = indTwo + indOne
#indFour = indThree + indOne

class imageAttrs:

    def __init__(self, srcDir, imageFilename):
        self.data = []
        #print  indThree + imageFilename
        imgFile = srcDir + "/" + imageFilename
        self.imgFile = imgFile
		
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
        self.exif_data = get_exif_data(image)        
        self.lat = get_lat(self.exif_data)   
        self.lon = get_lon(self.exif_data)   		
		
        print indFour + "Description : 	" + self.descr		
        print indFour + "mod time    : 	", self.modTime
        print indFour + "latitude    : ", self.lat
        print indFour + "longitude   : ", self.lon
        #get_field(image, "foo")
        return
		
