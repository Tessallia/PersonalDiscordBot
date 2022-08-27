import logging

import yt_dlp, asyncio, sqlite3, os, re
from logs.log import *
class music_downloader():

    SONGS = 'songs'
    ARCHIVE = 'a.txt'
    ydl_opts = {
           'format': 'bestaudio/best',
           'postprocessors': [{
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192',
           }],
        "outtmpl": SONGS+'/%(title)songs.%(ext)songs',
        'download_archive':ARCHIVE
       }



    #todo figure out if this needs to be async as well
    #todo create directory to put mp3s in
    #todo determine whether or not i should delete stuff that hasn't been used in a long time, or only delete when
    #   it starts to take up a lot of space and delete oldest and least used stuff.

    def __init__(self):

        self.logger = create_logger(__name__, logging.ERROR, os.curdirC)
        print('s')
        self.logger.error('sadf')

        if 'a.txt' not in os.listdir():
            with open(os.curdir + os.sep + self.ARCHIVE): pass
            self.logger.info("created archive file")
        if 'songs' not in os.listdir():
            os.mkdir(self.SONGS)
            self.logger.info("created song dir")

    def get_title(self, url):
        with yt_dlp.YoutubeDL({}) as ydl:
            return ydl.extract_info(url)["title"]
    def is_playlist(self, url):
        if "playlist?list=" in url:
            return True

    def check_songs(self,hash):
        for song in os.listdir('../songs'):
            if song.startswith(hash):
                return True
    def get_songpath(self, title):
        for song in os.listdir('../songs'):
            if song.startswith(title):
                return 'songs/'+song+".mp3"
    def get_playlist_songs(self, info):
        song_list = []
        for hash in info:
            for song in os.listdir('../songs'):
                if song.startswith(hash["id"]):
                    song_list.append('songs/'+song)
        return song_list

    def urlType(self, url):

        pass
    def get_info(self, url):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url)['entries']

        return info
    def get_song(self, url):
        """
        check database for song
        if song not in database call download
        """
        song = None

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(url)
            if self.is_playlist(url):
                song = self.get_playlist_songs(ydl.extract_info(url)['entries'])
            else:
                song = self.get_songpath(self.get_title(url))
            return song



    def process_input(self, input):
        """
        deturmine input type:
            song name##todo will get to this after getting url processign fully ironed out
                search youtube for song and get url to process
            url
                determine url type
                    single video
                        start on that song
                    playlist
                        playlist page
                        song in playlist

        :param url:
        :return:
        """