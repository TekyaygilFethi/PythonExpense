class TrainOpsDataTag():
    def __init__(self, startIndex,endIndex,tag,value):
        self.startIndex=startIndex
        self.endIndex=endIndex
        self.tag=tag
        self.value=value

    # def __str__(self):
    #     return "({},{},\"{}\")".format(self.startIndex,self.endIndex,self.tag)