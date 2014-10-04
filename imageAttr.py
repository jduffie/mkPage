from epil import *
import sys
from pageAttr import *
from imageAttr import *


def buildPageAttrs(srcDir):
    print srcDir
    jsonFile = open(srcDir + "/folder.json")
    attrs = pageAttr(jsonFile)
    #print attrs.description

def main(argv):
    # args = parseArgs(argv)
    # srcDir = args.srcDir[0])	
    srcDir = "/cygdrive/c/Users/jduffie/Pictures/Picasa/Exports/Europe2014/2014_09_07/EiffelTowerDinner"
    buildPageAttrs(srcDir)
    buildImageAttrs(srcDir, "France007.JPG")
    


################
if __name__ == "__main__":
    main(sys.argv[1:])
