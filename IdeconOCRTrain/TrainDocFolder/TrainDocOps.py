import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from IdeconOCRTrain.TrainJsonFolder.TrainJsonOps import AIJsonOps
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse

class AIDoc():
    def __init__(self, *args, **kwargs):
        self.jsonops=AIJsonOps()

    def write_to_file(self,objectList,isJson=False):
        try:
            with open("E:\\IdeconTrainDataFolder\\traindatas.txt", "r+") as file:
                if(isJson==True):
                    for obj in objectList:
                        file.write(obj+"\n")
                else:
                    for obj in objectList:
                        file.write(self.jsonops.jsonencode(obj)+"\n")         
        except Exception as e:
            raise Exception(str(e))

    def read_from_file(self):
        objectList=[]
        try:
            with open("E:\\IdeconTrainDataFolder\\traindatas.txt", "r") as file:
                for line in file:
                    objectList.append(self.jsonops.jsondecode(line))
            return objectList
        except Exception as e:
            raise Exception(str(e))