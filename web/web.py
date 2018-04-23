from flask import Flask, render_template, abort, jsonify, request, session,request, render_template, g, redirect, Response
import os
from server import rekognition as rek
from server import produce_voice as pro_v
from server import s3_operation as s3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "F:\a012018\iot\project\testimages"
pre_label = ""
image_path = "./static/image/temp/"

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
    img_name = os.listdir(image_path)[0]
    label = rek.label_detect(img_name)
    global pre_label
    if pre_label != label:
        pre_label = label
        path = "./static/audio/"
        pro_v.remove_old(path)
        audio_label = rek.getlabel(label)
        audio = path + pro_v.produce_audio(audio_label,path)
        return render_template("detect.html", image_label=label, audio_file=audio)
    else:
        return render_template("detect.html", image_label=label)



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
