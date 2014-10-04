import json

indOne = "    "

class pageAttr:

    def __init__(self, jsonFile):
        self.data = []
        self.jsonFile = jsonFile
        jsonDict = json.load(jsonFile)

        self.description = jsonDict["description"]
        self.location = jsonDict["location"]
        self.date = jsonDict["date"]
        print indOne + self.description		
        print indOne + self.location
        print indOne + self.date
        return
		
