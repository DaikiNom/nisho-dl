import PySimpleGUI as sg
from yt_dlp import YoutubeDL
import ctypes
import threading
import sys
import os
import image

# HDPI対応
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

# icon
icon = image.icon

# リソースパスを取得する
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)

# ffmpegのpath(/ffmpeg)
ffmpeg = resource_path('ffmpeg')

# ダウンロード
def download(options, urls):
    with YoutubeDL(options) as ydl:
        ydl.download(urls)

# 進捗状況を表示する
def progress_Bar(p):
    # progressbarの更新
    if p['status'] == 'downloading':
        window['progressbar'].update_bar(p['downloaded_bytes'] / p['total_bytes'] * 100)
        window['progress_text'].update(str(round(p['downloaded_bytes'] / p['total_bytes'] * 100)) + '%')
    elif p['status'] == 'finished':
        window['progressbar'].update_bar(100)
        window['progress_text'].update('100%')
    else:
        window['progressbar'].update_bar(0)
        window['progress_text'].update('0%')

def progress_BarforHighestQuality(p):
    # 初期化
    window['progressbar'].update_bar(0)
    # progressに使えるものがないので，ダウンロードが終わるまで待つ
    if p['status'] == 'finished':
        window['progressbar'].update_bar(100)
        window['progress_text'].update('100%')
    elif p['status'] == 'downloading':
        window['progressbar'].update_bar(0)
        window['progress_text'].update('Progress...')
    else:
        window['progressbar'].update_bar(0)
        window['progress_text'].update('0%')

sg.theme('DarkBrown1')

layout = [
    [sg.Push(),
        sg.Text('Nisho Downloader', size=(35, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE),
        sg.Push()],
    [sg.Text('リンク:'),
        sg.InputText(key='url')],
    # dl先のpathを指定する(デフォルトはダウンロードフォルダー)
    [sg.Text('保存先のパス:'),
        sg.InputText(key='path', readonly=True, text_color='black'),
        sg.FolderBrowse(button_text='参照', key='path_browse')],
    # 詳細設定
    [sg.Push(),
        sg.Text('詳細設定', size=(30, 1), justification='center', font=("メイリオ", 15), relief=sg.RELIEF_RIDGE),
        sg.Push()],
    [sg.Checkbox('プレイリストを逆順にダウンロードする', key='playlistreverse'),
        sg.Checkbox('字幕をダウンロードする', key='writesubitles')],
    [sg.Checkbox('ファイルサイズの上限を設定する', key='max_filesize'),
        sg.InputText(key='max_filesize_input', size=(10, 1)),
        sg.Text('MB')],
    [sg.Checkbox('ダウンロード数の上限を設定する', key='max_downloads'),
        sg.InputText(key='max_downloads_input', size=(10, 1)),],
    # 音声のみor動画をダウンロードするかを選択する
    [sg.Push(),
        sg.Button('動画をダウンロード', key='download_Video'),
        sg.Button('音声のみでダウンロード', key='download_Audio'),
        sg.Button('キャンセル', key='cancel'),
        sg.Push()],
    # 進捗状況を表示する
    [sg.Push(),
        sg.ProgressBar(100, orientation='h', size=(70, 10), key='progressbar'),
        sg.Text('0%', key='progress_text'),
        sg.Push()]
]

window = sg.Window('Nisho Downloader',
                    layout = layout,
                    icon = icon,
                    font = ("メイリオ", 11))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'download_Audio':
        # 連打防止
        window['download_Audio'].update(disabled=True)
        window['download_Video'].update(disabled=True)

        # options
        opts = {
            'format': 'bestaudio/best',
            'path': './',
            'outtmpl': os.path.join(values['path'], '%(title)s.wav'),
            'playlistreverse': values['playlistreverse'],
            'writesubitles': values['writesubitles'],
            'writeautomaticsub': values['writesubitles'],
            'break_on_existing': True,
            'live_from_start': True,
            # 進捗状況を表示する
            'progress_hooks': [progress_Bar],
            'ffmpeg_location': ffmpeg
        }

        # ファイルサイズの上限を設定する場合
        if values['max_filesize']:
            opts['max_filesize'] = values['max_filesize_input'] * 1000000
        # ダウンロード数の上限を設定する場合
        if values['max_downloads']:
            opts['max_downloads'] = values['max_downloads_input']
        

        if values['url'] != '':
            # ダウンロード開始
            threading.Thread(target=download, args=(opts, [values['url']])).start()
        else:
            sg.popup('URLを入力してください')

        # 連打防止
        window['download_Audio'].update(disabled=False)
        window['download_Video'].update(disabled=False)
    elif event == 'download_Video':
        # 連打防止
        window['download_Audio'].update(disabled=True)
        window['download_Video'].update(disabled=True)

        # options
        opts = {
            # mp4にして最高品質
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'path': './',
            'outtmpl': os.path.join(values['path'], '%(title)s.%(ext)s'),
            'playlistreverse': values['playlistreverse'],
            'writesubitles': values['writesubitles'],
            'writeautomaticsub': values['writesubitles'],
            'break_on_existing': True,
            'live_from_start': True,
            # 進捗状況を表示する
            'progress_hooks': [progress_BarforHighestQuality],
            'ffmpeg_location': ffmpeg
        }

        # ファイルサイズの上限を設定する場合
        if values['max_filesize']:
            opts['max_filesize'] = values['max_filesize_input'] * 1000000
        # ダウンロード数の上限を設定する場合
        if values['max_downloads']:
            opts['max_downloads'] = values['max_downloads_input']

        if values['url'] != '':
            threading.Thread(target=download, args=(opts, [values['url']])).start()
        else:
            sg.popup('URLを入力してください')

        # 連打防止
        window['download_Audio'].update(disabled=False)
        window['download_Video'].update(disabled=False)
    elif event == 'cancel':
        # 実行中のダウンロードをキャンセルする
        os.system('taskkill /f /im ffmpeg.exe')
        break
