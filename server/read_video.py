import cv2
import boto3
import _pickle as cPickle
import json
import time

config = json.load(open("./config.json"))
access_key = config["Access_Key"]
secret_key = config["Secret_Key"]
kinesis_shard = config["Kinesis_Shard_id"]
kinesis_client = boto3.client("kinesis",
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='us-east-1')
#rekog_client = boto3.client("rekognition")

config = json.load(open("./config.json"))
kinesis_name = config["Kinesis_Name"]
kinesis_shard = config["Kinesis_Shard_id"]
kinesis_type = "LATEST"


def read_video():
    shard_it = kinesis_client.get_shard_iterator(StreamName=kinesis_name,
        ShardId=kinesis_shard,
        ShardIteratorType=kinesis_type)["ShardIterator"]

    while(True):
        out = kinesis_client.get_records(ShardIterator=shard_it, Limit=1)
        shard_it = out["NextShardIterator"]
        frame = decode_image(out)
        time.sleep(1)
#cv2.imshow('frame', frame)



def decode_image(out):
    try:
        result = out["Records"][0]["Data"]
        flag = True
    except:
        print ('No Stream Now')
        flag = False
    if flag:
        frame_package = cPickle.loads(result, encoding='bytes')
        frame = frame_package[b'ImageBytes']
        decimg = cv2.imdecode(frame, 1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        return decimg

read_video()
