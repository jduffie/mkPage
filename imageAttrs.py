import json
from epil import *
indOne = "    "

class imageAttrs:

    def __init__(self, srcDir, imageFilename):
        self.data = []
        imgFile = srcDir + "/" + imageFilename
        self.imgFile = imgFile
		
        image = Image.open(imgFile)
        self.exif_data = get_exif_data(image)
        print get_lat_lon(self.exif_data)        
        return
		
