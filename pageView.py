
from mkPage_cmn import *
import os


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
            picStr += imageLineTemplate.format(im.imgFile, im.descr)
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/body.tmpl", "r") as tmplFile:
            bodyTmpl = tmplFile.read()
        self.bodyHtml = bodyTmpl.format(pm.title, pm.date, pm.location, pm.description, picStr)		
        #print self.bodyHtml
		
    def buildMap(self):	
        # build string containing the pic html
        with open (self.scriptDir + "/templates/pushpin.tmpl", "r") as tmplFile:
            pushpinTemplate = tmplFile.read()
		
        ppStr = ""
        for im in self.pageModel.imageModels:
            #print "Img Descr : ", im.descr
            ppStr += pushpinTemplate.format(im.imgFile, im.imgFile, im.lat, im.lon, im.descr)
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/map.tmpl", "r") as tmplFile:
            mapTmpl = tmplFile.read()
        self.mapHtml = mapTmpl.format(ppStr)		
        #print self.mapHtml
		