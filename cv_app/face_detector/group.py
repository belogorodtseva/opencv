import cognitive_face as CF
from fusioncharts import FusionCharts
from face_detector.models import *

KEY = '3f3fcb1528b14467bb1756614cd653e4'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

def best_emotion(face):

    emotionValues = [ face.emotions.sadness ,
                        face.emotions.neutral ,
                        face.emotions.contempt ,
                        face.emotions.disgust ,
                        face.emotions.anger ,
                        face.emotions.surprise ,
                        face.emotions.fear ,
                        face.emotions.happiness ]
    return(emotionValues.index(max(emotionValues)))

def group_detect(request,img_url,photo):

    url = img_url[1:]

    faces = CF.face.detect(url, face_id=True, landmarks=False, attributes='gender,emotion,smile')
    faceCount = 0
    maleCounter = 0
    femaleCounter = 0
    print (faces)

    for face in faces:
        faceOnGroup = FaceOnGroup()
        faceOnGroup.photo = photo
        emotionOnGroup = Emotion()
        fa = face["faceAttributes"]
        emotion = fa["emotion"]
        faceOnGroup.gender = fa["gender"]
        faceOnGroup.smile = fa["smile"]
        if fa["gender"] == 'female':
            femaleCounter+=1
        if fa["gender"] == 'male':
            maleCounter+=1
        emotions = []
        for e in emotion:
            emotions.append(emotion[e])
        emotionOnGroup.sadness = emotions[0]
        emotionOnGroup.neutral = emotions[1]
        emotionOnGroup.contempt = emotions[2]
        emotionOnGroup.disgust = emotions[3]
        emotionOnGroup.anger = emotions[4]
        emotionOnGroup.surprise = emotions[5]
        emotionOnGroup.fear = emotions[6]
        emotionOnGroup.happiness = emotions[7]
        emotionOnGroup.save()
        faceOnGroup.emotions = emotionOnGroup
        faceOnGroup.save()
        faceCount += 1

    if faceCount == 0:
        return(666)
    else:
        return([faceCount,maleCounter,femaleCounter])

def line_result(photo):
    faces = FaceOnGroup.objects.filter(photo=photo)
    array = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]
    resultA = []

    for face in faces:
        array[best_emotion(face)] += 1

    sumA = sum(array)

    for a in array:
        a = a*100/sumA
        resultA.append(a)

    return (resultA)


def draw_plots_all(photo):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    faces = FaceOnGroup.objects.filter(photo=photo)

    array = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]

    for face in faces:
        array[best_emotion(face)] += 1

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "ALL",
            "subCaption": "Group Emotions",
            "startingangle": "120",
            "showlabels": "0",
            "showlegend": "1",
            "enablemultislicing": "0",
            "slicingdistance": "40",
            "showpercentvalues": "1",
            "showpercentintooltip": "0",
            "theme": "ocean"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in emotionList:
      data = {}
      data['label'] = key
      data['value'] = str(array[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-3" , "100%", "400", "chart-3", "json", dataSource)

    return pie3d

def draw_plots_male(photo):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    faces = FaceOnGroup.objects.filter(photo=photo)

    maleArray = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]

    for face in faces:
        if face.gender == 'male':
            maleArray[best_emotion(face)] += 1

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "MALE",
            "subCaption": "Group Emotions",
            "startingangle": "120",
            "showlabels": "0",
            "showlegend": "1",
            "enablemultislicing": "0",
            "slicingdistance": "40",
            "showpercentvalues": "1",
            "showpercentintooltip": "0",
            "theme": "ocean"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in emotionList:
      data = {}
      data['label'] = key
      data['value'] = str(maleArray[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-2" , "100%", "400", "chart-2", "json", dataSource)

    return pie3d

def draw_plots_female(photo):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    faces = FaceOnGroup.objects.filter(photo=photo)

    femaleCounter = 0

    femaleArray = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]

    for face in faces:

        if face.gender == 'female':
            femaleArray[best_emotion(face)] += 1
            femaleCounter+=1

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "FEMALE",
            "subCaption": "Group Emotions",
            "startingangle": "120",
            "showlabels": "0",
            "showlegend": "1",
            "enablemultislicing": "0",
            "slicingdistance": "40",
            "showpercentvalues": "1",
            "showpercentintooltip": "0",
            "theme": "ocean"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in emotionList:
      data = {}
      data['label'] = key
      data['value'] = str(femaleArray[count])
      dataSource['data'].append(data)
      count+=1;

    # Create an object for the Column 2D chart using the FusionCharts class constructor
    pie3d = FusionCharts("pie3d", "ex-1" , "100%", "400", "chart-1", "json", dataSource)

    return pie3d

def draw_plots_male_smile(photo):
    smileList=['Unsmiling', 'Smiling']
    faces = FaceOnGroup.objects.filter(photo=photo)
    smileArray=[0,0]
    for face in faces:
        if face.gender == 'male':
            if face.smile <= 0.7 :
                smileArray[0] += 1
            else :
                smileArray[1] += 1
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "MALE",
            "subCaption": "Group Smiling",
            "startingangle": "120",
            "showlabels": "0",
            "showlegend": "1",
            "enablemultislicing": "0",
            "slicingdistance": "40",
            "showpercentvalues": "1",
            "showpercentintooltip": "0",
            "theme": "ocean"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in smileList:
      data = {}
      data['label'] = key
      data['value'] = str(smileArray[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-4" , "100%", "400", "chart-6", "json", dataSource)

    return pie3d

def draw_plots_female_smile(photo):
    smileList=['Unsmiling', 'Smiling']
    faces = FaceOnGroup.objects.filter(photo=photo)
    smileArray=[0,0]
    for face in faces:
        if face.gender == 'female':
            if face.smile <= 0.7 :
                smileArray[0] += 1
            else :
                smileArray[1] += 1
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "FEMALE",
            "subCaption": "Group Smiling",
            "startingangle": "120",
            "showlabels": "0",
            "showlegend": "1",
            "enablemultislicing": "0",
            "slicingdistance": "40",
            "showpercentvalues": "1",
            "showpercentintooltip": "0",
            "theme": "ocean"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in smileList:
      data = {}
      data['label'] = key
      data['value'] = str(smileArray[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-6" , "100%", "400", "chart-5", "json", dataSource)

    return pie3d

def draw_plots_all_smile(photo):
    smileList=['Unsmiling', 'Smiling']
    faces = FaceOnGroup.objects.filter(photo=photo)
    smileArray=[0,0]
    for face in faces:
        if face.smile <= 0.7 :
            smileArray[0] += 1
        else :
            smileArray[1] += 1
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "ALL",
            "subCaption": "Group Smiling",
            "startingangle": "120",
            "showlabels": "0",
            "showlegend": "1",
            "enablemultislicing": "0",
            "slicingdistance": "40",
            "showpercentvalues": "1",
            "showpercentintooltip": "0",
            "theme": "ocean"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in smileList:
      data = {}
      data['label'] = key
      data['value'] = str(smileArray[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-5" , "100%", "400", "chart-4", "json", dataSource)

    return pie3d
