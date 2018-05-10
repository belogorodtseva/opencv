import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cv2
import urllib, json
from os.path import expanduser
import matplotlib.pyplot as plt
import random


KEY = '2c88ec709ee943b49ac7c6202fad1a94'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

fnt = ImageFont.truetype('Roboto-Bold.ttf', 16)

vidcap = cv2.VideoCapture('video.mp4')
success,image = vidcap.read()
count = 1
numOfFrames = 0
numFrameToSave = 200
success = True
while success:
    if (numOfFrames % numFrameToSave ==0):
        cv2.imwrite("images/frame%d.jpg" % count, image)
        count += 1     # save frame as JPEG file
    success,image = vidcap.read()
    print 'Read a new frame: ', success
    numOfFrames += 1
resultArray = []
facesResult = "Video Result: \n \n"
emotionList = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']
count -= 1

while count > 0:

    frameArray= []
    frameArray.append(count)
    frameArray.append("_______")

    facesResult += "\n______________________________________________________\n"
    facesResult += "\n Frame #" + str(count) +":\n"

    img_url = "images/frame"+str(count)+".jpg"

    faces = CF.face.detect(img_url, face_id=True, landmarks=False, attributes='gender,emotion')

    faceCount = 0
    for face in faces:
        emotionValue = []
        fa = face["faceAttributes"]
        emotion = fa["emotion"]
        toShow="\n Face #" + str(faceCount) + "\n"
        for e in emotion:
            emotionValue.append(emotion[e])
            toShow+=e+"="+str(emotion[e])+"\n"
        color = ('#%06X' % random.randint(0,256**3-1))
        plt.plot(emotionList, emotionValue, color=color)
        facesResult += toShow
        faceCount +=1
        frameArray.append(faceCount)
        frameArray.append(emotionList)
        frameArray.append(emotionValue)
        frameArray.append("----------")

    resultArray.append("_________________\n")
    resultArray.append(count)
    resultArray.append("_______\n")
    resultArray.append(frameArray)
    resultArray.append("_________________\n")
    count -= 1

print(resultArray)
plt.title('Video result')
plt.show()
text_file = open("result.txt", "w+")
text_file.write(resultArray)
text_file.close()
