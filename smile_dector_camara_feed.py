import cv2
from io import BytesIO
from PIL import Image, ImageDraw
import requests
import os
# import time

apiKey = ':D'
region = "eastus"
baseUrl = "https://"+region+".api.cognitive.microsoft.com/face/v1.0/detect"

args = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'smile'
}


def GetSmileScore(frame):
    pil_img = Image.fromarray(frame)  # convert opencv frame
    stream = BytesIO()
    pil_img.save(stream, format='JPEG')
    bin_img = stream.getvalue()

    # Post the frame to the Face API
    headers = {'Content-Type': 'application/octet-stream',
               'Ocp-Apim-Subscription-Key': apiKey}
    response = requests.post(data=bin_img, url=ENDPOINT,
                             headers=headers, params=args)
    jsondata = response.json()

    smile = 0
#     print(jsondata)
    if jsondata and jsondata[0]:
        smile = jsondata[0]["faceAttributes"]["smile"]
    return smile


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FPS, 10)

while(True):
    ret, frame = cap.read()
    smile = GetSmileScore(frame)
    if smile < 0.7:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()