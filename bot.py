from telegram import File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from keys import telegram_token
from keys import *
import logging
from helpers import *
from helpers import text
import os
import subprocess

updater = Updater(token=telegram_token)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Calismaya Basladim")

def manane(bot, update):
    user = update.message.from_user
    isim = user.first_name
    print update.message
    gelen_mesaj = update.message.text
    if gelen_mesaj.startswith("/manane"):
        gelen_mesaj = gelen_mesaj[8:]
    cevrilmis = text_translator(gelen_mesaj)
    reply = isim + " der ki: " + cevrilmis
    update.message.reply_text(reply)
    add_log(gelen_mesaj.encode("utf-8"), cevrilmis.encode("utf-8"), isim.encode("utf-8"), str(update.message.chat_id), "text")


def message(bot, update):
    user = update.message.from_user
    isim = user.first_name
    gelen_mesaj = update.message.text
    print update.message
    cevrilmis = text_translator(gelen_mesaj)
    reply = isim + " der ki: " + cevrilmis
    update.message.reply_text(reply)
    add_log(gelen_mesaj.encode("utf-8"), cevrilmis.encode("utf-8"), isim.encode("utf-8"), str(update.message.chat_id), "group-text")

def voice(bot, update):
    audio_file = bot.getFile(update.message.voice["file_id"])
    voice_name = "voice_" + str(update.message.chat_id) + ".oga"
    audio_file.download(voice_name)
    convert_media(voice_name, "flac", 22050)
    voice_name = voice_name + ".flac"
    print voice_name
    subprocess.call(["gsutil", "cp", voice_name, "gs://syrapp/"+voice_name])
    subprocess.call(["gsutil", "acl", "ch", "-u", "AllUsers:R", ("gs://syrapp/" + voice_name)])
    try:
        sync_request("FLAC", 22050, "ar", ("gs://syrapp/" + voice_name))
        text_ar = text()
    except:
        text_ar = ["", 0]
    try:
        sync_request("FLAC", 22050, "tr", ("gs://syrapp/" + voice_name))
        text_tr = text()
    except:
        text_tr = ["", 0]
    lang = ""
    if float(str(text_ar[1])) > float(str(text_tr[1])):
        lang = "ar"
        metin = text_ar[0]
    else:
        lang = "tr"
        metin = text_tr[0]
    cevrilmis = text_translator_lang(metin, lang)
    out_file = str(voice_name) + ".aiff"
    TTS(cevrilmis, out_file, lang)
    convert_media(out_file, "oga")
    out_file = out_file + ".oga"
    isim = update.message.from_user.first_name
    print update.message
    update.message.reply_text(isim + " soyle soyledi: ")
    update.message.reply_text(metin)
    update.message.reply_voice(open(out_file, "r"))
    update.message.reply_text(cevrilmis)
    subprocess.call(["rm", ("*voice_"+str(update.message.chat_id)+"*")])
    add_log(metin.encode("utf-8"), cevrilmis.encode("utf-8"), isim.encode("utf-8"), str(update.message.chat_id), "voice")

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text, message)
voice_handler = MessageHandler(Filters.voice, voice)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(voice_handler)

updater.start_polling()