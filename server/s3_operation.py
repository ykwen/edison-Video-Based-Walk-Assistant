import boto3
import json
import datetime

config = json.load(open("../config.json"))
access_key = config["Access_Key"]
secret_key = config["Secret_Key"]
bucket = config["Bucket"]
client = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name='us-east-1')


def clear():
    objects = client.list_objects(Bucket=bucket, Prefix='/temp')['Contents']
    for object in objects:
        client.delete_object(Bucket=bucket, Key=object['Key'])
    return


def clear_face():
    objects = client.list_objects(Bucket=bucket, Prefix='/face')['Contents']
    for object in objects:
        client.delete_object(Bucket=bucket, Key=object['Key'])
    return


def upload(filepath):
    filename = filepath.split('/')[-1]
    client.upload_file(filepath, bucket, '/temp/'+ filename)
    return

def upload_face(filepath):
    filename = filepath.split('/')[-1]
    client.upload_file(filepath, bucket, '/face/' + filename)
    return

def save_face(filepath):
    filename = filepath.split('/')[-1]
    new_name = str(datetime.datetime.now())
    client.upload_file(filepath, bucket, 'save/' + new_name)
    return


def list_saved():
    prefix='save/'
    items = []
    res = client.list_objects(Bucket=bucket, Prefix=prefix)
    for cont in  res['Contents']:
        items.append(cont['Key'])
    return items
#upload('../web/static/image/temp/1524457073.jpg')
#clear()