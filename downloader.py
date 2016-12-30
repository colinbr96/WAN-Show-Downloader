#------------------------------------------------------------------------------
# IMPORTS

import json
from urllib.parse import urlencode
from collections import namedtuple

import requests # http://docs.python-requests.org/
import youtube_dl # https://github.com/rg3/youtube-dl/


#------------------------------------------------------------------------------
# CONSTANTS

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
DOWNLOADED_FILE = 'downloaded.json'
API_FILE = 'api.json'
PLAYLIST_ID = 'PL8mG-RkN2uTw7PhlnAr4pZZz2QubIbujH'
RESULTS_PER_REQUEST = 2


#------------------------------------------------------------------------------
# Globals

_downloaded = []
_api_key = ''

Video = namedtuple('Video', 'video_id title')


#------------------------------------------------------------------------------
# FUNCTIONS

def log(var):
    print(var)


def load_data():
    """ Opens the downloaded.json file and the api.json file
        Returns a 2-tuple (list(downloaded videos), str(API key))
    """
    global _downloaded, _api_key
    with open(DOWNLOADED_FILE) as json_data:
        d = dict(json.load(json_data))
        _downloaded = d['downloaded']

    with open(API_FILE) as json_data:
        d = dict(json.load(json_data))
        _api_key = d['api_key']
    

def save_data() -> None:
    """ Updates the download.json file with the given list(downloaded videos)
    """
    d = {'downloaded': _downloaded}
    with open(DOWNLOADED_FILE, 'w') as file:
        json.dump(d, file)


def get_videos() -> [Video]:
    """ Returns a list of Videos from the standard playlist ordered ascending
        in upload date
    """
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?'
    params = {
        'part':       'snippet',
        'maxResults': RESULTS_PER_REQUEST,
        'playlistId': PLAYLIST_ID,
        'key':        _api_key
    }
    url += urlencode(params)
    json_data = requests.get(url).json()

    videos = []
    for video in json_data['items']:
        snippet = video['snippet']
        video_id = snippet['resourceId']['videoId']
        title = snippet['title']
        videos.append(Video(video_id, title))
    return videos


def download_yt_video(video_id: str) -> None:
    """ Downloads the given YouTube URL using the standard config
    """
    url = 'https://www.youtube.com/watch?v=' + video_id
    print(url)
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.download([url])


def process_videos(videos: [Video]) -> None:
    """ Downloads the given videos and adds them to the _downloaded list
    """
    for v in videos:
        video_id = v.video_id
        if video_id not in _downloaded:
            download_yt_video(video_id)
            _downloaded.append(video_id)
        else:
            log("ERROR: " + video_id + " already downloaded.")


def upload_to_gdrive(files: dict):
    pass


#------------------------------------------------------------------------------
# MAIN

def main():
    load_data()
    videos = get_videos()
    process_videos(videos)
    save_data()


if __name__ == '__main__':
    main()
