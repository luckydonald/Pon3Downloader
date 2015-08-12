# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import sys  # launch arguments
from Pon3Downloader.sites.ponyFm import PonyFM
from Pon3Downloader.utilities.interactions import input, answer, confirm
from Pon3Downloader.utilities.store import Store, settings
from Pon3Downloader.utilities import do_complete_load_if_matches


def main(argv):
	import getpass
	if argv is None:
		argv = sys.argv[1:]  # argv[0] is program name
	if argv:
		url = argv[0]
	else:
		url = input("Url to download:")
	if not url:
		print("no url given.")
		sys.exit(0)
	if "use_login" not in settings or not settings.use_login:
		use_login = confirm("Use login with pony.fm command?\nYou can automatically fave and comment songs, and/or your download stats will be updated.", default=False)
		settings.use_login = use_login
		settings.save_settings()
		logger.debug("Saved use_login.")
	if settings.use_login:
		if "ponyfm_user" not in settings or not settings.ponyfm_user:
			default_username = getpass.getuser()
			username = answer("Username for pony.fm (poniverse.net)", default=default_username)
			settings.ponyfm_user = username
			settings.save_settings()
			logger.debug("Saved user.")
		else:
			username = settings.get("ponyfm_user")
		#end if
		store = Store()
		if "ponyfm_pass" not in settings or not settings.ponyfm_pass:
			print("Password for pony.fm (If your shell can't hide the input, a warning will be displayed)")
			__password = store.encrypt(getpass.getpass())
			if confirm("Safe password?", default=True):
				settings.ponyfm_pass = __password
				settings.save_settings()
				logger.info("Saved password.")
		else:
			__password = settings.get("ponyfm_pass")
		#end if
		ponyfm = PonyFM(username, password=__password, key=store.key)
	else:
		ponyfm = PonyFM
	do_complete_load_if_matches(ponyfm, url, cover_as_file=True)

if __name__ == "__main__":
	main(None)