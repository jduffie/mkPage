
from mkPage_cmn import *
import os
import re


class pageView:
    scriptDir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, pageModel):
        self.data = []
        self.pageModel = pageModel

        
    def prepStrForJscript(self, src):
        dst = ""
        if src != None:
            dst = src.replace("'", "\\'");
            dst = dst.replace('"', '\\"');
        return dst
        
    def linkifyString(self, src):
        if src == None:
            dst = ""
        else:            
            # replace html with links
            strList = src.split()
            dst = ""
            for strElem in strList:
                if "http://" in strElem:
                    strElem = '<a href="' + strElem + '">' + strElem + '</a>'
                dst += strElem + " "                                
        print indTwo + "linkifyString : ", dst
        return dst
        
    def buildBody(self):	
        # build string containing the pic html
        with open (self.scriptDir + "/templates/pic_line.tmpl", "r") as tmplFile:
            imageLineTemplate = tmplFile.read()
		
        picStr = ""
        for im in self.pageModel.imageModels:
            print indTwo + "Img Descr : ", im.descr
            strClean = self.linkifyString(im.descr)
            print indTwo + "strClean : ", strClean
            picStr += imageLineTemplate.format(im.imgFile, im.webFile, strClean)
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/body.tmpl", "r") as tmplFile:
            bodyTmpl = tmplFile.read()
        self.bodyHtml = bodyTmpl.format(pm.title, pm.date, pm.location, pm.description, picStr)		
        return self.bodyHtml		


		
    def buildMap(self):	        
        print indTwo + "buildMap: sat"
        self.mapSatHtml = ""
        if self.pageModel.imageModels:
            self.mapSatHtml = self.buildMapSat()
            
        print indTwo + "buildMap: route"
        self.mapRouteHtml = ""                            
        if self.pageModel.routeModels:
            self.mapRouteHtml = self.buildMapRoute()
                                
        pm = self.pageModel
        
        if self.mapSatHtml != "" or self.mapRouteHtml != "":
            print indTwo + "buildMap: writing map html"
            with open (self.scriptDir + "/templates/map.tmpl", "r") as tmplFile:
                mapTmpl = tmplFile.read()
            self.mapHtml = mapTmpl.format(self.mapSatHtml, self.mapRouteHtml)		
        else:
            self.mapHtml = ""
        return self.mapHtml
        
    def buildPushPinStrings(self):
        # build string containing the pic html
        with open (self.scriptDir + "/templates/pushpin.tmpl", "r") as tmplFile:
            pushpinTemplate = tmplFile.read()
    
        #print pushpinTemplate
        ppStr = ""
        for im in self.pageModel.imageModels:
            if im.lat and im.lon:
                #print "Img Descr : ", im.descr
                #print "    imgFile : ", im.imgFile
                #print "    lat : ", im.lat            
                #print "    lon : ", im.lon
                # strip all content from the period to end of line
                imageVarSuffix = re.sub("\..*$", '', im.imgFile)
                imageVarSuffix = imageVarSuffix.replace("-", "_");
                imageVarSuffix = imageVarSuffix.replace(" ", "_");
                print "    suffix : ", imageVarSuffix
                caption = self.prepStrForJscript(im.descr)                
                caption = self.linkifyString(caption)
                ppStr += pushpinTemplate.format(imageVarSuffix, im.lat, im.lon, caption)
        return ppStr

        
    def buildMapSat(self):	
        ppStr = self.buildPushPinStrings()
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/mapSat.tmpl", "r") as tmplFile:
            mapTmpl = tmplFile.read()
        latCenter,lonCenter = self.pageModel.imageCenter
        mapSatHtml = mapTmpl.format(ppStr,latCenter,lonCenter)		
        return mapSatHtml

        
    def buildMapRoute(self):	
        with open (self.scriptDir + "/templates/route.tmpl", "r") as tmplFile:
            routeTemplate = tmplFile.read()

        print routeTemplate
        rtStr = ""
        for rtFile in self.pageModel.routeModels:
                # strip all content from the period to end of line
                rtVarSuffix = re.sub("\..*$", '', rtFile)                               
                rtVarSuffix = rtVarSuffix.replace("-", "_");
                rtVarSuffix = rtVarSuffix.replace(" ", "_");
                #print "    suffix : ", rtVarSuffix
                rtStr += routeTemplate.format(rtVarSuffix, rtFile)
    
        ppStr = self.buildPushPinStrings()
		
        pm = self.pageModel
        # write string into the body.html with header args
        with open (self.scriptDir + "/templates/mapRoad.tmpl", "r") as tmplFile:
            mapTmpl = tmplFile.read()
        latCenter,lonCenter = self.pageModel.imageCenter
        mapRoadHtml = mapTmpl.format(ppStr,latCenter,lonCenter, rtStr)		
        return mapRoadHtml

    def buildTailMainColumn(self):	
        with open (self.scriptDir + "/templates/tailMainColumn.tmpl", "r") as tmplFile:
            tailMainColumnHtml = tmplFile.read()
        return tailMainColumnHtml

    def buildHeadMainColumn(self):	
        with open (self.scriptDir + "/templates/headMainColumn.tmpl", "r") as tmplFile:
            headMainColumnHtml = tmplFile.read()
        return headMainColumnHtml
        
    def buildSideMenu(self):	    
        sideMenuItems = ""                
        if self.pageModel.subPages != None:    
            
            with open (self.scriptDir + "/templates/sideMenuItem.tmpl", "r") as tmplFile:
                sideMenuItemTmpl = tmplFile.read()	       
            for pm in self.pageModel.subPages:
                if pm.subdir != ".":
                    print indTwo + "sideMenuItem: ", pm.title, " ", pm.subdir
                    sideMenuItems += sideMenuItemTmpl.format(pm.title, pm.description, pm.subdir)		

        sideMenuBack = ""                
        if self.pageModel.parentPageModel:
            pm = self.pageModel.parentPageModel
            print indTwo + "parentPageModel: title " + pm.title
            with open (self.scriptDir + "/templates/sideMenuBack.tmpl", "r") as tmplFile:
                sideMenuBackTmpl = tmplFile.read()	       
            sideMenuBack = sideMenuBackTmpl.format(pm.title, pm.description, pm.subdir)		
            print indTwo + "sideMenuBack " + sideMenuBack
                
        sideMenuHtml = ""
        with open (self.scriptDir + "/templates/sideMenu.tmpl", "r") as tmplFile:
            sideMenuTmpl = tmplFile.read()
        sideMenuHtml = sideMenuTmpl.format(sideMenuItems, sideMenuBack)		
        return sideMenuHtml

        
    def buildIndex(self):
        # build string containing the pic html
        with open (self.scriptDir + "/templates/index.tmpl", "r") as tmplFile:
            indexShtmlTemplate = tmplFile.read()
        #print "Index shtml : ", indexShtmlTemplate                
        self.indexShtml = indexShtmlTemplate
        return self.indexShtml
    