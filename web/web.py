import os
import cv2
from flask import Flask, render_template, abort, jsonify, request, session,request, render_template, g, redirect, Response
from server import rekognition as rek
from server import produce_voice as pro_v
from server import s3_operation as s3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "F:\a012018\iot\project\testimages"
pre_label = ""
label = ""
image_file = ""
image_path = "./static/image/temp/"
face_path = "./static/image/faces/"

@app.route('/')
def  index():
    return render_template('index.html')


@app.route('/show')
def show_image():
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'trafficsignal.jpg')
    image_file = os.listdir(image_path)[0]
    try:
        s3.clear()
    except:
        pass
    s3.upload(image_path+image_file)
    return render_template("show.html", user_image =image_path+image_file)


@app.route('/detect')
def detect_things():
    global image_file
    image_file = os.listdir(image_path)[0]
    try:
        s3.clear()
    except:
        pass
    s3.upload(image_path + image_file)
    global label
    label = rek.label_detect(image_file)
    global pre_label
    if set(pre_label) != set(label):
        pre_label = label
        path = "./static/audio/"
        pro_v.remove_old(path)
        audio_label = rek.getlabel(label)
        audio = path + pro_v.produce_audio(audio_label,path)
        return render_template("detect.html", image_label=label, audio_file=audio)
    else:
        return render_template("detect.html", image_label=label)


@app.route('/face',methods=['GET', 'POST'])
def detect_face():
    global label
    global image_file
    if "Human" in label:
        img = cv2.imread(image_path+image_file)
        img = rek.face_detect(image_file,img)
        cv2.imwrite(face_path+image_file,img)
        try:
            s3.clear_face()
        except:
            pass
        s3.upload_face(face_path + image_file)
    sub_status = "Click to Save the situation"
    if request.method == 'POST':
        s3.save_face(face_path + image_file)
        sub_status = "Situation saved"
    return render_template("face.html", user_image=face_path + image_file,sub_status=sub_status)

@app.route('/save')
def show_saved_face():
    items = s3.list_saved()
    return render_template("save.html", items=items)


if __name__ == '__main__':
    app.run()


'''
@app.route('/voice')
def voice_output():
    path = "./static/audio/"
    pro_v.remove_old(path)
    audio_label = rek.getlabel(label)
    audio = path + pro_v.produce_audio(audio_label,path)
    return render_template("detect.html",  audio_file=audio, image_label=label)
'''
