#!/usr/bin/env python3
import subprocess
from pathlib import Path
from typing import Union
import re
from ytmusicapi import YTMusic
import argparse

def read_songlist(input_txt_path: Union[str, Path]) -> list:
    input_txt_path = Path(input_txt_path)
    songlist = [item.strip() for item in input_txt_path.read_text().split('\n') if item.strip() != '']
    return songlist

def songs_download(songlist: list, output_dir_path: Path, ytmusic: YTMusic, format: str):
    for song in songlist:
        result = ytmusic.search(
            query=song,
            filter='songs',
            limit=1
        )
        video_id = result[0]['videoId']
        song = re.sub(r" ", r" ", song)
        subprocess.run([
            'yt-dlp',
            '--extract-audio', '--audio-format', format,
            '--audio-quality', '0',
            '--output', f'{output_dir_path}/{song}.{format}',
            f"https://music.youtube.com/watch?v={video_id}"])


def main():
    parser = argparse.ArgumentParser(description="Module for downloading songs from Youtube Music")
    parser.add_argument('song_list_path', help="path to .txt file containing the token to be search and download")
    parser.add_argument('output_dir_path', help="path to the output directory that will contain the downloaded songs")
    parser.add_argument('--format', '-f', type=str, choices=['mp3', 'wav'], default='mp3', help='choose output format')
    args = parser.parse_args()
    ytmusic = YTMusic()
    song_list_path = args.song_list_path
    output_dir_path = Path(args.output_dir_path)
    format = args.format
    song_list = read_songlist(song_list_path)
    if not output_dir_path.exists():
        output_dir_path.mkdir()
    songs_download(song_list, output_dir_path, ytmusic, format)
    
if __name__ == '__main__':
    main()
