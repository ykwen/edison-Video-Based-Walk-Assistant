from gtts import gTTS
import os
import time
import calendar

def produce_audio(labels,path):
    text = 'Attension, '
    for label in labels:
        text = text + ', '+ label
    text = text + ' in the front'
    tts = gTTS(text=text, lang='en')
    title = str(calendar.timegm(time.gmtime()))
    tts.save(path+title+".mp3")
    return title+".mp3"


def remove_old(path):
    for file_name in os.listdir(path):
        try:
            file_name = file_name.split('.')[0]
            if int(file_name) < calendar.timegm(time.gmtime()):
                os.remove(path+file_name+'.mp3')
        except:
            pass


'''
items = pd.read_csv("items.csv")

for item in items['name']:
    text = 'Attension, '+item+' in the front'
    tts = gTTS(text=text, lang='en')
    tts.save("../web/static/audio/"+item+".mp3")
'''