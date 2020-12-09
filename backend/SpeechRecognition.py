import speech_recognition as sr
import os

def recognizeSpeech():
    for filename in os.listdir("./chunks/"):
        if filename.endswith(".wav"): 
            r = sr.Recognizer()
            filenameWithoutFormat = filename[:-4]
            with sr.AudioFile("./chunks/" + filename) as source:
                audio = r.record(source)
                try:
                    rec = r.recognize_google(audio, language="ru")
                    f = open("./sentences/" + filenameWithoutFormat + "_sentence" + ".txt", "w+")
                    f.write(rec)
                    f.close()
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results. check your internet connection. Error: ", e)
            continue
        else:
            continue


# recognizeSpeech("chunk0.wav")