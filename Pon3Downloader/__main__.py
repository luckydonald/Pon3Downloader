# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import sys  # launch arguments


from Pon3Downloader.sites.ponyFm import PonyFM
from Pon3Downloader.sites.py_compatibility import input
from Pon3Downloader.utilities import do_complete_load
try:
	import secret_logins  # a file called secret_logins.py containing the password:  pony_fm = ("username", "password")
except ImportError:
	secret_logins = None

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
	if secret_logins:
		ponyfm = PonyFM(username=secret_logins.pony_fm[0], password=secret_logins.pony_fm[1])
	else:
		ponyfm = PonyFM
	do_complete_load(ponyfm, url, cover_as_file=True)


if __name__ == "__main__":
	main(None)