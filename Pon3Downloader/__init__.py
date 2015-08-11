# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import sys  # launch arguments


from sites.ponyFm import can_load, download_song
from sites.py_compatibility import input
from sites.utils import open_file_folder

def main(argv):
	if argv is None:
		argv = sys.argv[1:]  # argv[0] is program name
	if argv:
		url = argv[0]
	else:
		url = input("Url to download:")
	if not url:
		print("no url given.")
		sys.exit(0)

	song_id = can_load(url)
	if song_id:
		file = download_song(song_id)
		open_file_folder(file)
		print(file)
	else:
		print("Not valid url.")

if __name__ == "__main__":
	main(None)