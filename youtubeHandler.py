import youtube_dl, asyncio, sqlite3, os

class music_downloader():


    ydl_opts = {
           'format': 'bestaudio/best',
           'postprocessors': [{
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192',
           }],
       }
    #todo figure out if this needs to be async as well
    #todo create directory to put mp3s in
    #todo determine whether or not i should delete stuff that hasn't been used in a long time, or only delete when
    #   it starts to take up a lot of space and delete oldest and least used stuff.

    async def get_song(self, url):
        """
        check database for song
        if song not in database call download
        """
        pass

    def search_youtube(self):
        """
        pull first result for calls that aren't url to a specific song
        """

        pass

    def download(self, url):
        """
        download song
        get title
        convert to mp3 named with title
        save to database with url, title, and file path to mp3 file
        """
        pass

    def update_db(self):
        """
        Add newly downloaded mp3 (naming mp3 handled by download func) to song directory
        insert into db: url, title, file path for song
        """
        pass

    def trim_db(self):
        """
        find songs that have the least plays, or haven't been played in a long and delete them
        this function should be called by update when song directory gets too big.
        """
        pass


def get_stuff(something):
    for x in dir(something):
        print(x)

print(os.listdir('songs'))