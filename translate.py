# -*- coding: utf-8 -*-
from google.cloud import translate
from keys import *
import os

def ArabicText(file, form):
    curl = "curl -X POST -u " + bluemix_token + " --header 'Content-Type:audio/" + form + "' --data-binary @" + file + " 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=ar-AR_BroadbandModel'"
    data = os.popen(curl).read()
    import json
    json = json.loads(data)
    arabic_text = json["results"][0]["alternatives"][0]["transcript"]
    arabic_text = unicode(arabic_text)
    return arabic_text

def TurkishVoice(text, file):
    text = text.encode(encoding="utf-8")
    os.system("say -v Yelda -o " + file + " " + "'" + text + "'")

client = translate.Client(api_key=translate_key)

def target(dil):
    if dil == "ar":
        return "tr"
    elif dil == "tr":
        return "ar"

def text_translator(mesaj):
    m_dili = client.detect_language(mesaj)["language"]
    cevrilmis = client.translate(mesaj, target(m_dili))
    return cevrilmis["translatedText"]