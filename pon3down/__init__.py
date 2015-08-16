# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)


from Pon3Downloader import main as package
import sys
import os

def main(args=None):
	print(os.path.dirname(__file__))
	print(sys.path)
	package.main(args)