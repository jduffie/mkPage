import json

indOne = "    "
indTwo = indOne + indOne
indThree = indTwo + indOne

class pageAttrs:

    def __init__(self, jsonFile):
        self.data = []
        self.jsonFile = jsonFile
        jsonDict = json.load(jsonFile)

        self.description = jsonDict["description"]
        self.location = jsonDict["location"]
        self.date = jsonDict["date"]
        print indThree + self.description		
        print indThree + self.location
        print indThree + self.date
        return
		
