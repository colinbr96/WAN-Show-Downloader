# WAN-Show-Downloader
Downloads videos from the LinusTechTips YouTube channel, specifically the WAN Show playlist. The downloaded files are converted to MP3 and then uploaded to
Google Drive.

### Notes
   - The script is meant to be run on a weekly basis to check if any new videos
    have been added. It won't redownload videos that it has already downloaded.
   - JSON files are in my .gitignore so you must figure out how to create your own.

### Dependencies
   - [Requests](http://docs.python-requests.org/)
   - [YouTube DL](https://github.com/rg3/youtube-dl/)

### Files
   - `wan_show_downloader.py`: Main script
   - `downloaded.json`: Contains list of video IDs that have already been downloaded
   - `api.json`: Contains Google API key