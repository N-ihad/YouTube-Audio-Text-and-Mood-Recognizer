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
        emptyFolder(os.getcwd() + "/chunks")
        emptyFolder(os.getcwd() + "/sentences")
        emptyFolder(os.getcwd() + "/emotions")
        if os.path.exists(os.getcwd() + "/audio.mp3"):
            os.remove(os.getcwd() + "/audio.mp3")

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

        if len(os.listdir(os.getcwd() + "/samples_sentence") ) == 0:
            response = app.response_class(
                response=json.dumps({"message": "No such word was found"}),
                status=404,
                mimetype="application/json",
            )
            return response

        return send_file("samples_sentence.zip", mimetype='zip', attachment_filename='samples_sentence.zip', as_attachment=True)

class GenerateFilesByEmotion(Resource):
    def post(self):
        data = request.get_json(silent=True)
        emotionToSearch = {'emotionSearch': data.get('emotionSearch')}
        emotionToSearch = emotionToSearch["emotionSearch"]
        filterSamplesByEmotion(emotionToSearch)
        
        getZipForEmotionSamples()

        if len(os.listdir(os.getcwd() + "/samples_emotion") ) == 0:
            response = app.response_class(
                response=json.dumps({"message": "No such emotion was found"}),
                status=404,
                mimetype="application/json",
            )
            return response

        return send_file("samples_emotion.zip", mimetype='zip', attachment_filename='samples_emotion.zip', as_attachment=True)


api.add_resource(GenerateFiles, "/generate-files")
api.add_resource(GenerateFilesWithWord, "/generate-files-by-word")
api.add_resource(GenerateFilesByEmotion, "/generate-files-by-emotion")

if __name__ == "__main__":
    app.run(port=5002, debug=True)


