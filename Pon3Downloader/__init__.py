# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

VERSION = "0.0.4"
IDENTIFIER = "de.luckydonald.pon3downloader"


from usersettings import Settings
from luckydonaldUtils.store import random

settings = Settings(IDENTIFIER)  # store settings, password etc.
settings.add_setting("ponyfm_user", str, "")
settings.add_setting("ponyfm_pass", str, "")
settings.add_setting("use_login", bool, True)
settings.add_setting("do-not-change!", str, random())
settings.load_settings()  # get da settings.
settings.save_settings()  # write da settings. (new ones)
