from telegram import File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from keys import telegram_token
import logging
from helpers import *
import os
import time

from translate import *

updater = Updater(token=telegram_token)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Calismaya Basladim")

def message(bot, update):
    user = update.message.from_user
    isim = user.first_name
    gelen_mesaj = update.message.text
    reply = isim + " der ki: " + text_translator(gelen_mesaj)
    print type(reply)
    update.message.reply_text(reply)
    print isim, str(update.message.chat_id), reply
    try:
        log(gelen_mesaj, isim, update.message.chat_id)
        log(reply, isim, update.message.chat_id)
    except:
        pass

def audio(bot, update):
    audio_file = bot.getFile(update.message.audio["file_id"])
    audio_name = "audio_" + str(update.message.chat_id) + ".wav"
    audio_file.download(audio_name)
    cevrilmis = text_translator(ArabicText(audio_name, "wav"))
    out_file = str(audio_name) + ".aiff"
    TurkishVoice(cevrilmis, out_file)
    isim = update.message.from_user.first_name
    update.message.reply_text(isim + " soyle soyledi: ")
    update.message.reply_document(open(out_file, "r"))
    print isim, str(update.message.chat_id), cevrilmis
    try:
        log(cevrilmis, isim)
    except:
        pass

def voice(bot, update):
    audio_file = bot.getFile(update.message.voice["file_id"])
    voice_name = "voice_" + str(update.message.chat_id) + ".oga"
    audio_file.download(voice_name)
    #convert_media(voice_name, "ogg")
    #voice_name = voice_name + ".ogg"
    #time.sleep(10)
    #cevrilmis = text_translator(ArabicText(voice_name, "ogg"))
    #out_file = str(voice_name) + ".aiff"
    #TurkishVoice(cevrilmis, out_file)
    #convert_media(out_file, "ogg")
    #out_file = out_file + ".ogg"
    #isim = update.message.from_user.first_name
    #update.message.reply_text(isim + " soyle soyledi: ")
    #update.message.reply_voice(open(out_file, "r"))
    #print isim, str(update.message.chat_id), cevrilmis
    print "you're here"
    #bot.sendVoice(update.message.chat_id, open("voice.ogg", "r"))
    update.message.reply_voice(open("file.oga", "rb"))
    #update.message.reply_audio(open("voice_85920336.oga", "rb"))
    print "voice sent"

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text, message)
audio_handler = MessageHandler(Filters.audio, audio)
voice_handler = MessageHandler(Filters.voice, voice)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(audio_handler)
dispatcher.add_handler(voice_handler)


updater.start_polling()