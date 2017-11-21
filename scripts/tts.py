#!/usr/bin/python -tt

#
# Use google API for TTS
# Copyright (C) 2017, Qatar Computing Research Institute, HBKU (author: Ahmed Ali)
#

from gtts import gTTS
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Text To Speech Script')
    parser.add_argument('inputString', help='The input text')
    parser.add_argument('outputAudio', help='filename of the output audio')
    parser.add_argument("-l", "--language", help='chosen TTS language', type=str, required=False)
    parser.add_argument("-g", "--gender", help='male or female', type=str, required=False)
    
    args = parser.parse_args()
	
    tts = gTTS(text=args.inputString,lang='en')
    filename = args.outputAudio+'.wav'
    tts.save(filename)


