def DataTagToTuples(dataTags):
    tuples=[]
    for dataTag in dataTags:
        tpl=tuple(dataTag.startIndex,dataTag.endIndex,dataTag.tag)
        tuples.append(tpl)
    return tuples