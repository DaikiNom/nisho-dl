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
1. Get ffmpeg
   1. Download ffmpeg from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z).
   2. Extract the downloaded file.
   3. Move the `bin` folder to the root directory of this repository.
   4. Rename the `bin` folder to `ffmpeg`.
1. Build
    ```bash
    pyinstaller app.py --onefile -w -n NishoDownloader -i icon.png --add-data "./ffmpeg;./ffmpeg"
    ```

## License
This software is released under the AGPL-v3.0, see LICENSE.