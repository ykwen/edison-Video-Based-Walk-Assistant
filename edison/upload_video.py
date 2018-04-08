import sys
import datetime
import cv2
import boto3
import cPickle
import pytz
import json

kinesis_client = boto3.client("kinesis")
rekog_client = boto3.client("rekognition")

config = json.load(open("./edison/config.json"))
kinesis_name = config["Kinesis_Name"]
kinesis_shard = config["Kinesis_Shard_id"]


rekog_max_labels = 100
rekog_min_conf = 50.0


#Send frame to Kinesis stream
def encode_and_send_frame(frame, frame_count, enable_kinesis=True, enable_rekog=False, write_file=False):
    try:
        #convert opencv Mat to jpg image
        #print "----FRAME---"

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, encimg = cv2.imencode('.jpg', frame, encode_param)

        utc_dt = pytz.utc.localize(datetime.datetime.now())
        now_ts_utc = (utc_dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

        frame_package = {
            'ApproximateCaptureTime' : now_ts_utc,
            'FrameCount' : frame_count,
            'ImageBytes' : encimg
        }

        if write_file:
            print("Writing file img_{}.jpg".format(frame_count))
            target = open("img_{}.jpg".format(frame_count), 'w')
            target.write(img_bytes)
            target.close()

        #put encoded image in kinesis stream
        if enable_kinesis:
            print "Sending image to Kinesis"

            response = kinesis_client.put_record(
                StreamName=kinesis_name,
                Data=cPickle.dumps(frame_package),
                PartitionKey=kinesis_shard
            )

            print response

        if enable_rekog:
            response = rekog_client.detect_labels(
                Image={
                    'Bytes': img_bytes
                },
                MaxLabels=rekog_max_labels,
                MinConfidence=rekog_min_conf
            )
            print response
            return response

    except Exception as e:
        print e