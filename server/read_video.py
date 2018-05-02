import cv2
import boto3
import _pickle as cPickle
import json
import time
import calendar
import os

config = json.load(open("./config.json"))
access_key = config["Access_Key"]
secret_key = config["Secret_Key"]
kinesis_shard = config["Kinesis_Shard_id"]
kinesis_client = boto3.client("kinesis",
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='us-east-1')
kinesis_name = config["Kinesis_Name"]
kinesis_type = "LATEST"
image_path = "../web/static/image/temp/"


def remove_old(title):
    for file_name in os.listdir(image_path):
        try:
            file_name = file_name.split('.')[0]
            if int(file_name) < int(title.split('.')[0]):
                os.remove(image_path+file_name+'.jpg')
        except:
            pass


def read_video():
    shard_it = kinesis_client.get_shard_iterator(StreamName=kinesis_name,
        ShardId=kinesis_shard,
        ShardIteratorType=kinesis_type)["ShardIterator"]

    while(True):
        out = kinesis_client.get_records(ShardIterator=shard_it, Limit=1)
        shard_it = out["NextShardIterator"]
        frame, flag = decode_image(out)
        if flag:
            title = str(calendar.timegm(time.gmtime()))
            remove_old(title)
            cv2.imwrite(image_path+title+'.jpg',frame)
        time.sleep(1)



def decode_image(out):
    try:
        result = out["Records"][0]["Data"]
        flag = True
        print('Reading')
    except:
        print ('No Stream Now')
        flag = False
    if flag:
        frame_package = cPickle.loads(result, encoding='bytes')
        frame = frame_package[b'ImageBytes']
        decimg = cv2.imdecode(frame, 1)
        cv2.imshow('test',decimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        return decimg, flag
    else:
        return  [],flag


if __name__ == '__main__':
    read_video()