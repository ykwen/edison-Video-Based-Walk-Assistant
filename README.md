# Visual Safty Assistant

## IoT Project

### Group 1010

This is the IoT project for wearable device.

Use camera taking videos and streaming into aws for situation recognition.

#### Road

This part uses intel-edison with camera to stream video on to aws kinesis and use rekognition to analyze user's situation. If there is a potential danger around, it will raise a warning to remind users. If there is a criminal, users can choose the save the video and faces in the video for police department.

The stream video can also be displayed for logined users to show situation and recognition result.

The cascade data of traffic light is downloaded from https://github.com/cfizette/road-sign-cascades

#### Fall
If there is a fall signal detected by accelemeter from another part of the project, the server will send the picture received immediatly to related registed users.
