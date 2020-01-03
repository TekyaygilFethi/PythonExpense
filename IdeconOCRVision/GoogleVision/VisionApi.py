import io
import os
import copy
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import math

def detect_text(filePath):
    from google.cloud import vision
    from google.cloud.vision import types
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file('IdeconOCRVision\\GoogleVision\\credentials.json')

    # İstemciye çağrı başlatıyor.
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Resmin pathını alıyor
    # file_name = os.path.join(
    #     os.path.dirname(__file__),
    #     filePath)
    file_name=filePath

    # Görüntüyü belleğe yükler
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content) #changed

    response = client.document_text_detection(image=image)#changed
    yMax =  getYMax(response)

    data = invertAxis(response, yMax)
    lines = data.text_annotations[0].description.split('\n')
    rawText = data.text_annotations[1:]

    lines = lines[::-1]
    rawText = rawText[::-1]
    mergedArray = getMergedLines(lines, rawText)
    mergedArray = getBoundingPolygon(mergedArray)
    mergedArray = combineBoundingPolygon(mergedArray)
    return constructLineWithBoundingPolygon(mergedArray)

def constructLineWithBoundingPolygon(mergedArray):
    finalArray = []
    for i,item in enumerate(mergedArray):
        if (not mergedArray[i]['customValue']['matched']):
            if(len(mergedArray[i]['customValue']['match'])==0):
                finalArray.append(mergedArray[i]['trueValue'].description)
            else:
                finalArray.append(arrangeWordsInOrder(mergedArray, i))
    return finalArray

def arrangeWordsInOrder(mergedArray, k):
    mergedLine = ''
    wordArray = []
    line = mergedArray[k]['customValue']['match']
    for i,item in enumerate(line):
        index = line[i]['matchLineNum']
        matchedWordForLine = mergedArray[index]['trueValue'].description
        mainX = mergedArray[k]['trueValue'].bounding_poly.vertices[0].x
        compareX = mergedArray[index]['trueValue'].bounding_poly.vertices[0].x

        if (compareX > mainX):
            mergedLine = mergedArray[k]['trueValue'].description + ' ' + matchedWordForLine
        else:
            mergedLine = matchedWordForLine + ' ' + mergedArray[k]['trueValue'].description

    return mergedLine

#computes the maximum y coordinate from the identified text blob
def getYMax(data):
    v = data.text_annotations[0].bounding_poly.vertices
    yArray = []

    for i in range(4):
        yArray.append(v[i].y)

    return max(yArray)

#inverts the y axis coordinates for easier computation as the google vision starts the y axis from the bottom
def invertAxis(data,yMax):
    #data = fillMissingValues(data)
    index = 0
    for text in data.text_annotations:
        if index == 0:
            index = index + 1
            continue

        for j in range(4):
            b = (yMax - data.text_annotations[index].bounding_poly.vertices[j].y)
            data.text_annotations[index].bounding_poly.vertices[j].y = b

        index = index + 1

    return data

def fillMissingValues(data):
    for text in data.text_annotations[1::]:
        v = text.bounding_poly.vertices
        #burda v'nin y ve x değerleri undefined olanları 0 olarak atamak lazım değilse değiştirilmeyecek

    return  data

def getBoundingPolygon(mergedArray):
    newMergedArray=[]
    index = 0
    for merged in mergedArray:
        arr = []
        h1 = merged.bounding_poly.vertices[0].y - merged.bounding_poly.vertices[3].y
        h2 = merged.bounding_poly.vertices[1].y - merged.bounding_poly.vertices[2].y
        h = h1
        if h2>h1:
            h = h2

        avgHeight = h * 0.6

        arr.append(merged.bounding_poly.vertices[1])
        arr.append(merged.bounding_poly.vertices[0])
        line1 = getRectangle(copy.deepcopy(arr), True, avgHeight, True)

        arr = []
        arr.append(merged.bounding_poly.vertices[2])
        arr.append(merged.bounding_poly.vertices[3])
        line2 = getRectangle(copy.deepcopy(arr), True, avgHeight, False)


        customValue = {}
        customValue['lineNum'] = index
        customValue['bigbb'] = createRectCoordinates(line1, line2)
        customValue['match'] = []
        customValue['matched'] = False

        newArray = {}
        newArray['customValue'] = customValue
        newArray['trueValue'] = merged
        #merged['lineNum'] = index
        #merged['bigbb'] = createRectCoordinates(line1, line2)
        #merged['match'] = []
        #merged['matched'] = ""
        newMergedArray.append(newArray)
        index = index + 1
    return newMergedArray

def combineBoundingPolygon(mergedArray):
    for i,item in enumerate(mergedArray):
        bigBB = mergedArray[i]['customValue']['bigbb']
        k=i
        for item2 in mergedArray:
            if(k==len(mergedArray)):
                break

            if(k != i and mergedArray[k]['customValue']['matched']== False):
                insideCount = 0
                for j in range(4):
                    coordinate = mergedArray[k]['trueValue'].bounding_poly.vertices[j]
                    #b =  bigBB.contains(Point(coordinate.x, coordinate.y))
                    if(inside(coordinate.x, coordinate.y,bigBB)):
                        insideCount = insideCount + 1

                if (insideCount == 4):
                    match = {"matchCount": insideCount, "matchLineNum": k}
                    mergedArray[i]['customValue']['match'].append(match)
                    mergedArray[k]['customValue']['matched'] = True
            k= k+1
    return mergedArray

def inside(x,y,poly):
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def createRectCoordinates(line1,line2):
    return [[line1['xMin'], line1['yMin']], [line1['xMax'], line1['yMax']], [line2['xMax'], line2['yMax']], [line2['xMin'], line2['yMin']]]

def getRectangle(v,isRoundValues, avgHeight, isAdd):

    if(isAdd):
        v[1].y = round(v[1].y + avgHeight)
        v[0].y = round(v[0].y + avgHeight)
    else:
        v[1].y = round(v[1].y - avgHeight)
        v[0].y = round(v[0].y - avgHeight)

    yDiff = (v[1].y - v[0].y)
    xDiff = (v[1].x - v[0].x)

    gradient = yDiff / xDiff
    xThreshMin = 1
    xThreshMax = 2000

    yMin = 0
    yMax = 0

    if(gradient == 0):
        yMin = v[0].y
        yMax = v[0].y
    else:
        yMin = (v[0].y) - (gradient * (v[0].x - xThreshMin))
        yMax = (v[0].y) + (gradient * (xThreshMax - v[0].x))

    if(isRoundValues):
        yMin = round(yMin)
        yMax = round(yMax)

    value = {}
    value['xMin'] = xThreshMin
    value['xMax'] = xThreshMax
    value['yMin'] = yMin
    value['yMax'] = yMax

    return value

def getMergedLines(lines, rawText):
    mergedArray = []
    while len(lines) != 1:
        l = lines[-1]
        l1 = copy.deepcopy(lines[-1])
        del lines[-1]
        status = True

        mergedElement = {}

        while(True):
            if not rawText:
                break

            wElement = rawText[-1]
            del rawText[-1]

            w = wElement.description

            index = l.find(w)
            l = l[index + len(w)::]
            if (status):
                status=False
                mergedElement = wElement

            if (l == ""):
                mergedElement.description = l1
                mergedElement.bounding_poly.vertices[1].x = wElement.bounding_poly.vertices[1].x
                mergedElement.bounding_poly.vertices[1].y = wElement.bounding_poly.vertices[1].y
                mergedElement.bounding_poly.vertices[2].x = wElement.bounding_poly.vertices[2].x
                mergedElement.bounding_poly.vertices[2].y = wElement.bounding_poly.vertices[2].y
                mergedArray.append(mergedElement)
                break
    return mergedArray