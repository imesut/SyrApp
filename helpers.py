# -*- coding: utf-8 -*-
import os

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

def convert_media(file, format):
    command = "ffmpeg -i " + str(file) + " " + str(file) + "." + format
    os.system(command)