# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging  # pip install luckydonald-utils
logger = logging.getLogger(__name__)


def do_complete_load_if_matches(plugin, url, cover_as_file=True):
	song_id = plugin.can_load(url)
	if song_id:
		file = plugin.download_song(song_id, cover_as_file=cover_as_file)
		return file


class Plugin(object):
	def can_load(self, url):
		raise  NotImplementedError("can_load not implemented by plugin.")

	def download_song(self, song_id):
		"""
		Returns a file path.
		:param song_id:
		:return:
		"""
		raise NotImplementedError("download_song not implemented by plugin.")