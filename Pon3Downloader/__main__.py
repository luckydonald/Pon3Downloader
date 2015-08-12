# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import sys  # launch arguments
from usersettings import Settings # pip install usersettings

from Pon3Downloader.sites.ponyFm import PonyFM
from Pon3Downloader.utilities.interactions import input, answer, confirm
from Pon3Downloader.utilities import do_complete_load_if_matches
from Pon3Downloader import VERSION, IDENTIFIER
settings = Settings(IDENTIFIER)  # store settings, password etc.

try:
	import secret_logins  # a file called secret_logins.py containing the password:  pony_fm = ("username", "password")
except ImportError:
	secret_logins = None

def main(argv):
	import getpass
	settings.load_settings()  # get da settings.
	if argv is None:
		argv = sys.argv[1:]  # argv[0] is program name
	if argv:
		url = argv[0]
	else:
		url = input("Url to download:")
	if not url:
		print("no url given.")
		sys.exit(0)
	if "use_login" not in settings:
		use_login = confirm("Use login with pony.fm command?\nYou can automatically fave and comment songs, and/or your download stats will be updated.", default=False)
		settings.add_setting("use_login", bool, use_login)
		settings.use_login = use_login
	if settings.use_login:
		if "username" not in settings:
			default_username = getpass.getuser()
			username = answer("username for pony.fm (poniverse.net)", default=default_username)
			settings.add_setting("ponyfm_user", str, username)
			settings.ponyfm_user = username
		if "password" not in settings:
			print("Password for pony.fm (If your shell can't hide the input, a warning will be displayed)")
			__password = getpass.getpass()
			settings.add_setting("ponyfm_pass", str, __password)
			settings.ponyfm_pass = __password



		ponyfm = PonyFM(username=secret_logins.pony_fm[0], password=secret_logins.pony_fm[1])
	else:
		ponyfm = PonyFM
	do_complete_load_if_matches(ponyfm, url, cover_as_file=True)

if __name__ == "__main__":
	main(None)