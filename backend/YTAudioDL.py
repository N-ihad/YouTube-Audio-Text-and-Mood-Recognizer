# from __future__ import unicode_literals
# import youtube_dl

# def downloadYTAudio(link):
#     ydl_opts = {
#     'format': 'bestaudio/best',
#     'outtmpl': 'audio.mp3',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '320',
#     }]}

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])

# # downloadYTAudio("https://www.youtube.com/watch?v=i6bxLlf3Vbc")

from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import ffmpeg

def downloadYTAudio(link):
    YouTube(link).streams.filter(only_audio=True).first().download(filename='audio')
    command2mp3 = "ffmpeg -y -i audio.mp4 audio.mp3"
    os.system(command2mp3)
    os.remove("audio.mp4")