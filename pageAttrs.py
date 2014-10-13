import json
import os
from mkPage_cmn import *

class pageAttrs:

    def __init__(self, jsonFileName):
        self.data = []
        jsonFile = open(jsonFileName)
        self.jsonFile = jsonFile
        print "new json file ", jsonFile
        jsonDict = json.load(jsonFile)
        #print json.dumps(jsonDict)
        self.title = jsonDict["title"]
        self.description = jsonDict["description"]
        self.location = jsonDict["location"]
        self.date = jsonDict["date"]
        self.subdir = os.path.dirname(jsonFileName)
        print indFour + self.title		
        #print indThree + self.location
        #print indThree + self.date
        return

    def setImageModels(self, imgModels):
        self.imageModels = imgModels

    def setRouteModels(self, routeModels):
        self.routeModels = routeModels

    def setImageCenter(self, imgCenter):
        self.imageCenter = imgCenter
        
    def setSubPageModel(self, subPages):
        self.subPages = subPages
        
    def setParentPageModel(self, parent):
        self.parentPageModel = parent
        
        
        
        
