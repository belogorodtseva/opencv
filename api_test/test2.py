import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import cv2


KEY = '2c88ec709ee943b49ac7c6202fad1a94'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = 'https://image.freepik.com/fotos-gratis/feliz-ou-triste_430-19315432.jpg'


faces = CF.face.detect(img_url, face_id=True, landmarks=False, attributes='gender,emotion')
fnt = ImageFont.truetype('Roboto-Bold.ttf', 16)


#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


#Convert width height to a point in a rectangle
def getEmotionLocation(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']+5
    top = rect['top']+5
    return ((left, top))



#Download the image from the url
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

#For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red')
    fa = face["faceAttributes"]
    emotion = fa["emotion"]
    toShow=""
    for e in emotion:
        toShow+=e+"="+str(emotion[e])+"\n"
    print(toShow)
    draw.text(getEmotionLocation(face), toShow, font=fnt, fill='lime')


#Display the image in the users default image browser.
img.show()
