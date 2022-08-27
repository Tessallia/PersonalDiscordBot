import concurrent.futures
import logging
import yt_dlp, asyncio, sqlite3, os, re
from logs.log import *


class music_downloader():
    #todo set up regex to fix song titles that can't be saved directly as file names liek
    #   i've no more F***s to give.mp3. saves as i've not more F_s to give.mp3
    #   anythig with \ / : * ? " < > | in it must be changed to hve underscores
    SONGS = 'songs'
    ARCHIVE = 'a.txt'
    ydl_opts = {
           'format': 'bestaudio/best',
           'postprocessors': [{
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192',
           }],
        "outtmpl": SONGS+'/%(title)s.%(ext)s',
        'download_archive':ARCHIVE,
        'quiet':True
       }

    def __init__(self):

        self.logger = create_logger(__name__, logging.ERROR, os.curdir+os.sep+'logs')

        if 'a.txt' not in os.listdir():
            with open(os.curdir + os.sep + self.ARCHIVE): pass
            self.logger.info("created archive file")
        if 'songs' not in os.listdir():
            os.mkdir(self.SONGS)
            self.logger.info("created song dir")

    def fix_title(self, string):
        return re.sub(r'[\\/:*?"<>|]+', "_", string)



    def get_info(self, url):
        print("#################info#####################")

        with yt_dlp.YoutubeDL({'quiet':True}) as ydl:
            info = ydl.extract_info(url, download=False)
        songs = []

        try:
            entries = info['entries']
            for entry in entries:
                songs.append(self.fix_title(entry['title']), entry['webpage_url'])
            return songs
        except:
            #for _ in info.keys(): print(_)
            return [self.fix_title(info["title"]), info['original_url']]

    def download_url(self, url):
        print("##################download####################")
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download(url)
                return True
        except Exception as e:
            self.logger.error(e)

    #def get_songs(self, url):
#
    #    songs = []
    #    with concurrent.futures.ThreadPoolExecutor() as executor:
    #        download = executor.submit(self.download_url, url)
    #        info = executor.submit(self.get_info, url)
#
    #        entries = info.result()['entries']
    #        for entry in entries:
    #            songs.append('songs' + os.sep + entry['title'] + '.mp3')
    #        download.done()
    #    return songs
