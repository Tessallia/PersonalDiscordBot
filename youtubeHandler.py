import yt_dlp, asyncio, sqlite3, os

class music_downloader():

    SONGS = 'songs'
    ydl_opts = {
           'format': 'bestaudio/best',
           'postprocessors': [{
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192',
           }],
        "outtmpl": SONGS+'/%(id)s-%(title)s.%(ext)s',
        'download_archive':'a.txt'
       }
    #todo figure out if this needs to be async as well
    #todo create directory to put mp3s in
    #todo determine whether or not i should delete stuff that hasn't been used in a long time, or only delete when
    #   it starts to take up a lot of space and delete oldest and least used stuff.

    def __init__(self):
        pass
    def get_title(self, url):
        with yt_dlp.YoutubeDL({}) as ydl:
            return ydl.extract_info(url)["title"]

    def get_hash(self, url):
        return url.split("watch?v=", 1)[1]

    def is_playlist(self, url):
        if "playlist?list=" in url:
            return True

    def check_songs(self,hash):
        for song in os.listdir('songs'):
            if song.startswith(hash):
                return True
    def get_songpath(self, hash):
        for song in os.listdir('songs'):
            if song.startswith(hash):
                return 'songs/'+song
    def get_playlist_songs(self, info):
        song_list = []
        print(info)
        for hash in info:
            for song in os.listdir('songs'):
                if song.startswith(hash["id"]):
                    song_list.append('songs/'+song)
        return song_list

    def get_song(self, url):
        """
        check database for song
        if song not in database call download
        """
        song = None
#        if not self.is_playlist(url):
#            if not self.check_songs(self.get_hash(url)):
#                print("dl")
#                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                    ydl.download(url)
#        else:
#            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
#                ydl.download(url)
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(url)
            if self.is_playlist(url):
                song = self.get_playlist_songs(ydl.extract_info(url)['entries'])
            else:
                song = self.get_songpath(self.get_hash(url))
            print(song)
            return song


u2= "https://www.youtube.com/watch?v=IkIhgb-wgmM"
url = "https://www.youtube.com/watch?v=7H-71p9vieI"
lis = "https://www.youtube.com/playlist?list=PL_gcregDRpNvYOVyLQ9i9tfuNDatXj4w4"
u3 = "https://www.youtube.com/playlist?list=PL_gcregDRpNvYOVyLQ9i9tfuNDatXj4w4"
