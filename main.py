import sys
import os
import shutil
from typing import Dict

from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def get_metadata(file_path: str) -> Dict:
    if file_path.lower().endswith(".flac"):
        audio = FLAC(file_path)
    elif file_path.lower().endswith(".mp3"):
        audio = MP3(file_path, ID3=EasyID3)
    else:
        return "Unsupported file type"

    metadata = {tag: audio[tag] for tag in audio.keys()}
    metadata['filename'] = file_path
    return metadata


def organize(metadata: Dict):
    dir_name = os.path.join(organized_dir, metadata['artist'][0])
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    year = metadata.get('year') or metadata.get('date')
    dir_name = os.path.join(dir_name, f"{year[0]} - {metadata['album'][0]}")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    song_name = f"{metadata['tracknumber'][0]} - {metadata['title'][0]}"
    end_goal = os.path.join(dir_name, song_name)
    if not os.path.exists(end_goal):
        shutil.copy(metadata['filename'], end_goal)
        print(f"{end_goal} organized")


unorganized_dir = sys.argv[1]
organized_dir = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]

file_metadata = []
for file in os.listdir(unorganized_dir):
    if not os.path.isdir(file):
        file_metadata.append(get_metadata(os.path.join(unorganized_dir, file)))


for metadata in file_metadata:
    organize(metadata)