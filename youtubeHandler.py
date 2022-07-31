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
       }
    #todo figure out if this needs to be async as well
    #todo create directory to put mp3s in
    #todo determine whether or not i should delete stuff that hasn't been used in a long time, or only delete when
    #   it starts to take up a lot of space and delete oldest and least used stuff.


    def get_title(self, url):
        with yt_dlp.YoutubeDL({}) as ydl:
            return ydl.extract_info(url)["title"]

    def get_hash(self, url):
        return url.split("watch?v=", 1)[1]

    def check_songs(self,hash):
        for song in os.listdir('songs'):
            if song.startswith(hash):
                return True
    def get_songpath(self, hash):
        for song in os.listdir('songs'):
            if song.startswith(hash):
                return 'songs/'+song
    def get_song(self, url):
        """
        check database for song
        if song not in database call download
        """
        if not self.check_songs(self.get_hash(url)):
            print("dl")
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download(url)

        return self.get_songpath(self.get_hash(url))

u2= "https://www.youtube.com/watch?v=IkIhgb-wgmM"
url = "https://www.youtube.com/watch?v=7H-71p9vieI"
