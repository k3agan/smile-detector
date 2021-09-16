from io import BytesIO
from PIL import Image, ImageDraw,ImageFont
import requests
import json
import pprint
import operator

apiKey = ':)'
region = "eastus"
baseUrl = "https://"+region+".api.cognitive.microsoft.com/face/v1.0"

args = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,emotion,smile'
}

headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': apiKey}    

# Load image and convert to bytes
pil_img = Image.open('Images/steve.jpg')
stream = BytesIO()
pil_img.save(stream, format='JPEG') # convert PIL Image to Bytes
bin_img = stream.getvalue()

# Detect faces
detectEndpoint = baseUrl+"/detect"
detectResponse = requests.post(data=bin_img, url=detectEndpoint, headers=headers, params=args)
faces = detectResponse.json()


def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

def getEmotion(faceDictionary):
    emotions = faceDictionary['faceAttributes']['emotion']
    sorted_x = sorted(emotions.items(), key=operator.itemgetter(1),reverse=True)
    emotion,score = sorted_x[0]
    return emotion

draw = ImageDraw.Draw(pil_img)
font = ImageFont.truetype("arial.ttf", 30)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red',width=3)
    
    textPosition = (face['faceRectangle']['left'],face['faceRectangle']['top'] + face['faceRectangle']['height'])
    feeling = getEmotion(face)
    age = face['faceAttributes']['age']
    gender = face['faceAttributes']['gender']
    draw.text(textPosition,"Age: {0}\nFeeling: {1}\nGender: {2}".format(age,feeling,gender),font=font,fill=(255,0,0,255))    

pil_img.show()    
