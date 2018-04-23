import cv2
import boto3
import json
import time
import pandas as pd

config = json.load(open("../config.json"))
access_key = config["Access_Key"]
secret_key = config["Secret_Key"]
bucket = config["Bucket"]
client = boto3.client("rekognition",
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='us-east-1')

items= pd.read_csv("../server/items.csv")


def label_detect(fileName):
    s3_path = "/temp/"
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': s3_path+fileName}},MinConfidence=60)
    labels = []
    for label in response['Labels']:
        if label['Confidence'] >= 60:
            labels.append(label['Name'] )
    #print(labels)
    return labels


def getlabel(label):
    rlabel = []
    for item in items['name']:
        if item in label:
            rlabel.append(item)
    return rlabel



def mark_faces(fdata, img):
    height, width,_ = img.shape
    print (width, height)
    for item in fdata:
        x1 = int(item[2]*width)
        y1 = int(item[3]*height)
        x2 = x1 + int(item[0]*width)
        y2 = y1 + int(item[1]*height)
        img = cv2.rectangle(img, (x1,y1), (x2,y2),(255,0,0), 2)
    return img


face_features = ['Width','Height','Left','Top']
def face_detect(fileName, img):
    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}})
    faces = response['FaceDetails']
    face_data = []
    for bound in faces:
        fd = []
        for feature in face_features:
            fd.append(bound['BoundingBox'][feature])
        face_data.append(fd)

    img = mark_faces(face_data, img)

    return response
'''
    cv2.imshow('test',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass
    time.sleep(100)
'''

if __name__ == "__main__":
    for name in items['name']:
        print(name)
    '''
    fileName = 'walkingpeople.jpeg'
    img = cv2.imread('../../testimages/'+fileName)
    face_detect(fileName,img)
    '''