
from mkPage_cmn import *
import os
import re


class pageView:
    scriptDir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, pageModel):
        self.data = []
        self.pageModel = pageModel

    def buildBody(self):	
        # build string containing the pic html
        with open (self.scriptDir + "/templates/pic_line.tmpl", "r") as tmplFile:
            imageLineTemplate = tmplFile.read()
		
        picStr = ""
        for im in self.pageModel.imageModels:
            print "Img Descr : ", im.descr
            picStr += imageLineTemplate.format(im.imgFile, im.webFile, im.descr)
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/body.tmpl", "r") as tmplFile:
            bodyTmpl = tmplFile.read()
        self.bodyHtml = bodyTmpl.format(pm.title, pm.date, pm.location, pm.description, picStr)		
        return self.bodyHtml		
        #print self.bodyHtml
		
    def buildMap(self):	        
        if self.pageModel.imageModels:
            self.buildMapSat()
        else:
            self.mapSatHtml = ""
        # print " self.buildMapSat()   ", self.buildMapSat()   
        self.buildMapRoad()    
        # print " self.buildMapRoad()   ", self.buildMapRoad()           
        pm = self.pageModel
        # write string into the body.html with header args
        
        if self.mapSatHtml != "" or self.mapRoadHtml != "":
            with open (self.scriptDir + "/templates/map.tmpl", "r") as tmplFile:
                mapTmpl = tmplFile.read()
            self.mapHtml = mapTmpl.format(self.mapSatHtml, self.mapRoadHtml)		
        else:
            self.mapHtml = ""
        return self.mapHtml
        
    def buildMapSat(self):	
        # build string containing the pic html
        with open (self.scriptDir + "/templates/pushpin.tmpl", "r") as tmplFile:
            pushpinTemplate = tmplFile.read()

        print pushpinTemplate
        ppStr = ""
        for im in self.pageModel.imageModels:
            if im.lat and im.lon:
                #print "Img Descr : ", im.descr
                #print "    imgFile : ", im.imgFile
                #print "    lat : ", im.lat            
                #print "    lon : ", im.lon
                # strip all content from the period to end of line
                imageVarSuffix = re.sub("\..*$", '', im.imgFile)
                print "    suffix : ", imageVarSuffix
                ppStr += pushpinTemplate.format(im.imgFile, im.imgFile, im.lat, im.lon, im.descr, imageVarSuffix)
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/mapSat.tmpl", "r") as tmplFile:
            mapTmpl = tmplFile.read()
        latCenter,lonCenter = self.pageModel.imageCenter
        self.mapSatHtml = mapTmpl.format(ppStr,latCenter,lonCenter)		
        return self.mapSatHtml
        
    def buildMapRoad(self):	
        # build string containing the pic html
        with open (self.scriptDir + "/templates/pushpin.tmpl", "r") as tmplFile:
            pushpinTemplate = tmplFile.read()

        print pushpinTemplate
        ppStr = ""
        for im in self.pageModel.imageModels:
            if im.lat and im.lon:
                #print "Img Descr : ", im.descr
                #print "    imgFile : ", im.imgFile
                #print "    lat : ", im.lat            
                #print "    lon : ", im.lon
                # strip all content from the period to end of line
                imageVarSuffix = re.sub("\..*$", '', im.imgFile)
                print "    suffix : ", imageVarSuffix
                ppStr += pushpinTemplate.format(im.imgFile, im.imgFile, im.lat, im.lon, im.descr, imageVarSuffix)
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/mapRoad.tmpl", "r") as tmplFile:
            mapTmpl = tmplFile.read()
        latCenter,lonCenter = self.pageModel.imageCenter
        self.mapRoadHtml = mapTmpl.format(ppStr,latCenter,lonCenter)		
        return self.mapRoadHtml
        
    def buildIndex(self):
        # build string containing the pic html
        with open (self.scriptDir + "/templates/index.shtml", "r") as tmplFile:
            indexShtmlTemplate = tmplFile.read()
        #print "Index shtml : ", indexShtmlTemplate                
        self.indexShtml = indexShtmlTemplate
        return self.indexShtml
    