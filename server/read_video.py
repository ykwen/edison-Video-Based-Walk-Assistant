import cv2
import boto3
import cPickle
import json
import time

kinesis_client = boto3.client("kinesis")
rekog_client = boto3.client("rekognition")

config = json.load(open("./edison/config.json"))
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



    #frame = decode_image(response)
    #cv2.imshow('frame', frame)



def decode_image(out):
    try:
        result = out["Records"][0]["Data"]
        flag = True
    except:
        print 'No Stream Now'
        flag = False
    if flag:
        frame_package = cPickle.loads(result)
        frame = frame_package['ImageBytes']
        decimg = cv2.imdecode(frame, 1)
        return decimg

read_video()
