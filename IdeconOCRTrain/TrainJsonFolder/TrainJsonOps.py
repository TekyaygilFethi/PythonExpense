import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
from IdeconOCRData.TrainOpsDataFolder.TrainOpsData import TrainOpsData

class AIJsonOps():
    def jsonencode(self,obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
               return {'__tuple__': True, 'items': item}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                return {key: hint_tuples(value) for key, value in item.items()}
            else:
               return item
        return json.JSONEncoder().encode(hint_tuples(obj.__dict__))

    def hinted_tuple_hook(self,obj):
        if '__tuple__' in obj:
          return tuple(obj['items'])
        else:
            return obj

    def jsondecode(self,jsonString):
        expectedObject=TrainOpsData(trainData=json.loads(jsonString.replace(", null",""), object_hook=self.hinted_tuple_hook))
    
        for counter in range(0,len(expectedObject.trainData["trainData"][1]["entities"])):
            expectedObject.trainData["trainData"][1]["entities"][counter]=tuple(expectedObject.trainData["trainData"][1]["entities"][counter])
        return expectedObject
