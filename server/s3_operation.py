import boto3
import json

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


def upload(filepath):
    filename = filepath.split('/')[-1]
    client.upload_file(filepath, bucket, '/temp/'+ filename)
    return

#upload('../web/static/image/temp/1524457073.jpg')
#clear()