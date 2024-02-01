# NishoDownloader
## Description
NishoDownloader is a simple downloader for downloading files from the internet.
It is written in Python and uses the [yt-dlp](https://github.com/yt-dlp/yt-dlp) library for downloading files.

## How to use
1. Enter the URL of the file you want to download.
1. Press the `Download Movie` button or `Download Audio` button.

### Extra options
- You can select the download destination from the `Browse` button.
- You can download playlists in reverse order by checking the checkbox.
- You can download subtitles by checking the checkbox.
- Check the checkbox for file size limit, enter the file size, and files larger than that size will not be downloaded.
- Check the checkbox for download limit, enter the number of downloads, and files larger than that number will not be downloaded.

## How to build
1. Install requirements
    ```bash
    pip install -r requirements.txt
    ```
    If you want to install the packages yourself, install the following packages.
    - yt-dlp
    - pySimpleGUI
    - pyinstaller
2. Get ffmpeg
   1. Download or build ffmpeg.
   2. Create a folder named `ffmpeg` in the same directory as the `app.py` file.
   3. Move the `ffmpeg.exe` file to the `ffmpeg` folder.
3. Build
    ```bash
    pyinstaller app.py -w -n NishoDownloader -i icon.png --add-data "./ffmpeg;./ffmpeg"
    ```

## License
This software is released under the GPL-v3.0, see LICENSE.