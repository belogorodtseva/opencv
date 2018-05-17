import cognitive_face as CF
from fusioncharts import FusionCharts
from face_detector.models import *
import cv2
import requests
from django.core.files import File

KEY = '3f1480ceef0742bd8e317e72473b0ca6'  # Replace with a valid subscription key (keeping the quotes in place).
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

def best_emotion_faces(faces):

    emotionValues = [ 0,0,0,0,0,0,0,0 ]
    for face in faces:
        emotionValues[0] += face.emotions.sadness
        emotionValues[1] += face.emotions.neutral
        emotionValues[2] += face.emotions.contempt
        emotionValues[3] += face.emotions.disgust
        emotionValues[4] += face.emotions.anger
        emotionValues[5] += face.emotions.surprise
        emotionValues[6] += face.emotions.fear
        emotionValues[7] += face.emotions.happiness
    return(emotionValues.index(max(emotionValues)))

def video_cut(url,video):
    print (url)
    vidcap = cv2.VideoCapture(url[1:])
    success,image = vidcap.read()
    count = 1
    numOfFrames = 0
    numFrameToSave = 25
    success = True

    while success:

        if (numOfFrames % numFrameToSave ==0):
            frame = FramePhoto()
            frame.video = video
            cv2.imwrite("media/frame%d.jpg" % count, image)
            reopen = open("media/frame%d.jpg" % count, "rb")
            django_file = File(reopen)
            frame = FramePhoto()
            frame.video = video
            frame.image.save('image.jpg', django_file, save=True)
            result = frame_detect(frame, "media/frame%d.jpg" % count)
            print (result)
            print 'save'
            count += 1     # save frame as JPEG file

        success,image = vidcap.read()
        numOfFrames += 1
    count -= 1

def frame_detect(frame,url):

    faces = CF.face.detect(url, face_id=True, landmarks=False, attributes='gender,emotion')
    faceCount = 0
    maleCounter = 0
    femaleCounter = 0

    for face in faces:
        faceOnFrame = Face()
        faceOnFrame.frame = frame
        emotionOnFace = Emotion()
        fa = face["faceAttributes"]
        emotion = fa["emotion"]
        faceOnFrame.gender = fa["gender"]
        if fa["gender"] == 'female':
            femaleCounter+=1
        if fa["gender"] == 'male':
            maleCounter+=1
        emotions = []
        for e in emotion:
            emotions.append(emotion[e])
        emotionOnFace.sadness = emotions[0]
        emotionOnFace.neutral = emotions[1]
        emotionOnFace.contempt = emotions[2]
        emotionOnFace.disgust = emotions[3]
        emotionOnFace.anger = emotions[4]
        emotionOnFace.surprise = emotions[5]
        emotionOnFace.fear = emotions[6]
        emotionOnFace.happiness = emotions[7]
        emotionOnFace.save()
        faceOnFrame.emotions = emotionOnFace
        faceOnFrame.save()
        faceCount += 1

    if faceCount == 0:
        return(666)
    else:
        return([faceCount,maleCounter,femaleCounter])

def draw_plot_video(video):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    array = [ 0, 0 ,0, 0, 0, 0, 0, 0 ]

    videoFrames = FramePhoto.objects.filter(video=video)

    for frame in videoFrames:
        faces = Face.objects.filter(frame=frame)

        for face in faces:
            array[best_emotion(face)] += 1

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "VIDEO",
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

    dataSource['data'] = []
    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 0;
    for key in emotionList:
      data = {}
      data['label'] = key
      data['value'] = str(array[count])
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("pie3d", "ex-7" , "100%", "400", "chart-7", "json", dataSource)

    return pie3d

def draw_line_video(video):
    emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']

    frames = []
    videoFrames = FramePhoto.objects.filter(video=video)

    for frame in videoFrames:
        faces = Face.objects.filter(frame=frame)
        frames.append(best_emotion_faces(faces))

    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = {}
    dataSource['chart'] = {
        "caption": "VIDEO",
            "subCaption": "Emotions",
            "caption": "FRAMES",
            "subCaption": "Emotions",
            "showValues": "0",
            "rotateLabels": "1",
            "slantLabels": "1",
            "showHoverEffect": "1",
            "canvasPadding": "10",
            "showaxislines": "1",
            "anchorRadius": "4",
            "anchorHoverRadius": "8",
            "theme": "carbon"
        }

    # The data for the chart should be in an array where each element of the array is a JSON object
    # having the `label` and `value` as key value pair.

    dataSource['data'] = []

    # Iterate through the data in `Revenue` model and insert in to the `dataSource['data']` list.
    count = 1;
    for f in frames:
      data = {}
      data['value'] = int(f)
      #data['displayValue'] = emotionList[f]
      data['label'] = str(str(count) + 'frame')
      dataSource['data'].append(data)
      count+=1;

    pie3d = FusionCharts("line", "ex-8" , "100%", "400", "chart-8", "json", dataSource)

    return pie3d
