# -*- coding: utf-8 -*-
import os
from google.cloud import translate
from keys import *
import json
import datetime

log_file = open("log.txt", "a")
def log(text, *args):
    info = ""
    for i in args:
        info = str(i) + " # " + str(info)
    log_file.write("###: ")
    log_file.write(info)
    log_file.write("| ")
    log_file.write(str(text))
    log_file.write("\n")

def target(dil):
    if dil == "ar":
        return "tr"
    elif dil == "tr":
        return "ar"

def convert_media(file, target, sample=0):
    if target == "oga":
        command = "ffmpeg -y -i " + str(file) + " -acodec libopus " + str(file) + ".oga"
    elif sample>0:
        command = "ffmpeg -y -i " + str(file) + " -ar " + str(sample) + " " + str(file) + "." + str(target)
    else:
        command = "ffmpeg -y -i " + str(file) + " " + str(file) + "." + str(target)
    os.system(command)

def TTS(text, file, lang):
    text = text.encode(encoding="utf-8")
    if lang == "ar":
        say = "say -v Yelda -o " + file + " " + "'" + text + "'"
    else:
        say = "say -v Maged -o " + file + " " + "'" + text + "'"
    os.system(say)

client = translate.Client(api_key=translate_key)

def text_translator(mesaj):
    m_dili = client.detect_language(mesaj)["language"]
    cevrilmis = client.translate(mesaj, target(m_dili))
    return cevrilmis["translatedText"]

def text_translator_lang(mesaj, lang):
    m_dili = lang
    cevrilmis = client.translate(mesaj, target(m_dili))
    return cevrilmis["translatedText"]

def sync_request(e, s, l, u):
    filename = 'sync-request.json'
    with open(filename, 'w') as f:
        data = {}
        data["config"] = {}
        data["config"]["encoding"] = e
        data["config"]["sampleRate"] = s
        data["config"]["languageCode"] = l
        data["audio"] = {}
        data["audio"]["uri"] = u
        f.write(json.dumps(data))

def text():
    curl = 'curl -s -k -H "Content-Type: application/json" -H "Authorization: Bearer ' + speech_access_token + '" https://speech.googleapis.com/v1beta1/speech:syncrecognize -d @sync-request.json'
    root = json.load(os.popen(curl))
    print root
    root = root["results"][0]["alternatives"][0]
    try:
        return [root["transcript"], root["confidence"]]
    except:
        return [root["transcript"], 0]

def add_log(message, translate, name, chat_id, type):
    with open("log.txt", "a") as f:
        f.write("mesaj: " + message)
        f.write("\n")
        f.write("çeviri: " + translate)
        f.write("\n")
        f.write("isim: " + name + " " + str(chat_id))
        f.write("\n")
        f.write(str(datetime.datetime.now()))
        f.write("\n")
        f.write(type)
        f.write("\n\n")