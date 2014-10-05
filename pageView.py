
from mkPage_cmn import *
import os

imageLineTemplate = "<p> <a href=\"{0}\"> <img SRC=\"{0}_med.jpg\"> </a> \n \
<p>   {1} \n \
<hr>" 

class pageView:

    def __init__(self, pageModel):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.data = []
        self.pageModel = pageModel

        # build string containing the pic html
        picStr = ""

        for imageModel in pageModel.imageModels:
            print "Img Descr : ", imageModel.descr
            picStr += imageLineTemplate.format(imageModel.imgFile, imageModel.descr)
		
        with open (scriptDir + "/templates/body.tmpl", "r") as tmplFile:
            bodyTmpl = tmplFile.read()
        self.bodyHtml = bodyTmpl.format(pageModel.title, pageModel.date, pageModel.location, pageModel.description, picStr)
        print self.bodyHtml
		
