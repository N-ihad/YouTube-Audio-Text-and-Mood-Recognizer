from flask import Flask, jsonify, request, send_file, make_response, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from datetime import datetime
import json
import datetime
import time
import os
import sys
from YTAudioDL import downloadYTAudio
from SilenceBasedAudioSplit import splitAudioBySilence
from SpeechRecognition import recognizeSpeech
from EmotionRecognition import recognizeEmotion
from EmptyFolder import emptyFolder
from PrepareZip import getZip, getZipForWordSamples, getZipForEmotionSamples
from sampleFilter import filterSamplesByWord, filterSamplesByEmotion


app = Flask(__name__)
CORS(app)
api = Api(app)


class GenerateFiles(Resource):
    def post(self):
        emptyFolder("/Users/nihad/Desktop/Grid and Cloud/chunks")
        emptyFolder("/Users/nihad/Desktop/Grid and Cloud/sentences")
        emptyFolder("/Users/nihad/Desktop/Grid and Cloud/emotions")
        if os.path.exists("/Users/nihad/Desktop/Grid and Cloud/audio.mp3"):
            os.remove("/Users/nihad/Desktop/Grid and Cloud/audio.mp3")

        data = request.get_json(silent=True)
        ytLink = {'link': data.get('link')}
        ytLink = ytLink["link"]

        downloadYTAudio(ytLink)
        splitAudioBySilence("audio.mp3")
        recognizeSpeech()
        recognizeEmotion()

        getZip()

        return send_file("samples.zip", mimetype='zip', attachment_filename='samples.zip', as_attachment=True)

class GenerateFilesWithWord(Resource):
    def post(self):
        data = request.get_json(silent=True)
        wordToSearch = {'wordSearch': data.get('wordSearch')}
        wordToSearch = wordToSearch["wordSearch"]
        filterSamplesByWord(wordToSearch)

        getZipForWordSamples()

        return send_file("samples_sentence.zip", mimetype='zip', attachment_filename='samples_sentence.zip', as_attachment=True)

class GenerateFilesByEmotion(Resource):
    def post(self):
        data = request.get_json(silent=True)
        emotionToSearch = {'emotionSearch': data.get('emotionSearch')}
        emotionToSearch = emotionToSearch["emotionSearch"]
        filterSamplesByEmotion(emotionToSearch)
        
        getZipForEmotionSamples()

        return send_file("samples_emotion.zip", mimetype='zip', attachment_filename='samples_emotion.zip', as_attachment=True)


api.add_resource(GenerateFiles, "/generate-files")
api.add_resource(GenerateFilesWithWord, "/generate-files-by-word")
api.add_resource(GenerateFilesByEmotion, "/generate-files-by-emotion")

if __name__ == "__main__":
    app.run(port=5002, debug=True)


