import shutil, os
from EmptyFolder import emptyFolder

def filterSamplesByWord(word):
    emptyFolder("./samples_sentence/")
    for filename in os.listdir("./sentences/"):
        if filename.endswith(".txt"): 
            flname = filename[0:filename.find('_')]
            with open("./sentences/" + filename) as f:
                if word in f.read():
                    shutil.copy("./sentences/" + filename, './samples_sentence')
                    shutil.copy("./chunks/" + flname + ".wav", "./samples_sentence")
                    shutil.copy("./emotions/" + flname + "_emotion.txt", "./samples_sentence")
                    continue
            continue
        else:
            continue

def filterSamplesByEmotion(emotion):
    emptyFolder("./samples_emotion/")
    for filename in os.listdir("./emotions/"):
        if filename.endswith(".txt"): 
            flname = filename[0:filename.find('_')]
            with open("./emotions/" + filename) as f:
                if emotion in f.read():
                    shutil.copy("./emotions/" + filename, './samples_emotion')
                    shutil.copy("./chunks/" + flname + ".wav", "./samples_emotion")
                    shutil.copy("./sentences/" + flname + "_sentence.txt", "./samples_emotion")
            continue
        else:
            continue