from io import BytesIO
from os.path import basename
from zipfile import ZipFile
import time
import os

def getZip():
    with ZipFile('samples.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk("/Users/nihad/Desktop/Grid and Cloud/chunks"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        for folderName, subfolders, filenames in os.walk("/Users/nihad/Desktop/Grid and Cloud/sentences"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        for folderName, subfolders, filenames in os.walk("/Users/nihad/Desktop/Grid and Cloud/emotions"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        zipObj.close()
    return zipObj

def getZipForWordSamples():
    with ZipFile('samples_sentence.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk("/Users/nihad/Desktop/Grid and Cloud/samples_sentence"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        zipObj.close()
    return zipObj

def getZipForEmotionSamples():
    with ZipFile('samples_emotion.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk("/Users/nihad/Desktop/Grid and Cloud/samples_emotion"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
        zipObj.close()
    return zipObj