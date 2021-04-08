import os
import sys
import argparse
from mp3_tagger import MP3File
import re
import shutil

"""Move mp3 files to dst directory.
Dst directory should already exist, before program starts"""

parser = argparse.ArgumentParser(usage="sorter.py [OPTIONS]")
parser.add_argument("-s", "--src-dir", help="TEXT  Source directory", type=str, default="./")
parser.add_argument("-d", "--dst-dir", help="TEXT  Destination directory", type=str, default="./")
args = parser.parse_args()

try:
    directory_content = os.listdir(os.path.join(args.src_dir))
except Exception:
    print("No such source directory")
    sys.exit(0)

try:
    _ = os.listdir(args.dst_dir)
except Exception:
    print("No such destination directory")
    sys.exit(0)

tag_template = "[A-Za-zА-Яа-я\ -_]+"
prohibited_symbols = '\\/*|<>?:"'
id3_file_tags = dict()
for file_name in directory_content:
    try:
        mp3 = MP3File(os.path.join(args.src_dir, file_name))
    except Exception as e:
        print(e)
        continue
    id3_file_tags[file_name] = dict()
    tags = mp3.get_tags()
    for version in tags.keys():
        for id in tags[version]:
            if (tags[version][id]):
                if (isinstance(tags[version][id], str)):
                    if (re.match(tag_template, tags[version][id])):
                        pole = tags[version][id].strip()
                        for symbol in prohibited_symbols:
                            pole = pole.replace(symbol, "")
                        id3_file_tags[file_name][id] = pole
                elif (not isinstance(tags[version][id], type(None))):
                    id3_file_tags[file_name][id] = tags[version][id]

    if (not ("artist" in id3_file_tags[file_name] and "album" in id3_file_tags[file_name])):
        del id3_file_tags[file_name]

for file_name in id3_file_tags.keys():
    try:
        os.mkdir(os.path.join(args.dst_dir, id3_file_tags[file_name]["artist"]))
    except Exception as e:
        pass

    try:
        os.mkdir(os.path.join(args.dst_dir, id3_file_tags[file_name]["artist"], id3_file_tags[file_name]["album"]))
    except Exception as e:
        pass

    name = id3_file_tags[file_name]["song"] + ".mp3" if ("song" in id3_file_tags[file_name]) else file_name

    try:
        shutil.move(os.path.join(args.src_dir, file_name),
                    os.path.join(args.dst_dir, id3_file_tags[file_name]["artist"],
                                 id3_file_tags[file_name]["album"], name))
        print(os.path.join(args.src_dir, file_name), "\t->\t",
              os.path.join(args.dst_dir, id3_file_tags[file_name]["artist"],
                           id3_file_tags[file_name]["album"], name))
    except Exception as e:
        print(e)
print("Done")