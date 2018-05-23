import cognitive_face as CF
from fusioncharts import FusionCharts
from face_detector.models import *
import cv2
import requests
from django.core.files import File

KEY = '45849a53156a4f59a7fa8848d734824f'  # Replace with a valid subscription key (keeping the quotes in place).
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

def diary_detect(request,img_url,photo):

    url = img_url[1:]

    faces = CF.face.detect(url, face_id=True, landmarks=False, attributes='emotion')
    faceCount = 0

    for face in faces:
        emotionOnDiary = Emotion()
        fa = face["faceAttributes"]
        emotion = fa["emotion"]

        emotions = []
        for e in emotion:
            emotions.append(emotion[e])
        emotionOnDiary.sadness = emotions[0]
        emotionOnDiary.neutral = emotions[1]
        emotionOnDiary.contempt = emotions[2]
        emotionOnDiary.disgust = emotions[3]
        emotionOnDiary.anger = emotions[4]
        emotionOnDiary.surprise = emotions[5]
        emotionOnDiary.fear = emotions[6]
        emotionOnDiary.happiness = emotions[7]
        emotionOnDiary.save()
        photo.emotions = emotionOnDiary
        photo.save()
        faceCount += 1

    if faceCount == 0:
        return(666)
    else:
        return(emotions)

def draw_pie_plot(user):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    array = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]

    photos = DiaryPhoto.objects.filter(user=user)

    for face in photos:
        array[(best_emotion(face))] += 1

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "DIARY",
            "subCaption": "Emotions",
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
    print (array)
    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in emotionList:
      data = {}
      data['label'] = key
      data['value'] = str(array[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-10" , "100%", "400", "chart-10", "json", dataSource)

    return pie3d

def draw_line_plot(user):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    diary = []
    photos = DiaryPhoto.objects.filter(user=user)

    for face in photos:
        diary.append(best_emotion(face))

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "PHOTOS",
            "subCaption": "Emotions",
            "showValues": "0",
            "yAxisName": "EMOTIONS",
            "slantLabels": "1",
            "showHoverEffect": "1",
            "canvasPadding": "10",
            "showaxislines": "1",
            "anchorRadius": "5",
            "anchorHoverRadius": "15",
            "anchorBgColor": "#ffffff",
            "lineThickness": "2",
            "paletteColors": "#0075c2",
            "plotHoverEffect":"1",
            "baseFontColor": "#333333",
            "captionFontSize": "14",
            "subcaptionFontSize": "14",
            "subcaptionFontBold": "0",
            "showBorder": "0",
            "bgColor": "#ffffff",
            "showShadow": "0",
            "canvasBgColor": "#ffffff",
            "canvasBorderAlpha": "0",
            "divlineAlpha": "100",
            "divlineColor": "#999999",
            "divlineThickness": "1",
            "divLineDashed": "1",
            "divLineDashLen": "1",
            "showXAxisLine": "1",
            "xAxisLineThickness": "1",
            "xAxisLineColor": "#999999",
            "toolTipBgColor": "#ffffff",
            "showToolTipShadow": "1"

        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []

    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 1;
    for f in diary:
      data = {}
      data['value'] = int(f)
      data['label'] = str(str(count) + 'day')
      data['toolText'] = str(emotionList[f])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("line", "ex-11" , "100%", "400", "chart-11", "json", dataSource)

    return pie3d
