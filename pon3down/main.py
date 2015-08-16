# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

from Pon3Downloader import main as pon3dl_main
import sys
import os

def main(args=None):
	print(os.path.dirname(__file__))
	print(sys.path)
	pon3dl_main.main(args)