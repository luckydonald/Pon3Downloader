# -*- coding: utf-8 -*-
__author__ = 'luckydonald'


from luckydonaldUtils.store import random
from Pon3Downloader import IDENTIFIER

import logging

logger = logging.getLogger(__name__)


from usersettings import Settings # pip install usersettings
settings = Settings(IDENTIFIER)  # store settings, password etc.
settings.add_setting("ponyfm_user", str, "")
settings.add_setting("ponyfm_pass", str, "")
settings.add_setting("use_login", int, -1)
settings.add_setting("do-not-change!", str, random())
settings.load_settings()  # get da settings.
settings.save_settings()  # write da settings. (new ones)
