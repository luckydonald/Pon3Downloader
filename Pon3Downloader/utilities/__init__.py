# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from .files import open_file_folder

def do_complete_load(plugin, url, cover_as_file=True):
	song_id = plugin.can_load(url)
	if song_id:
		file = plugin.download_song(song_id, cover_as_file=cover_as_file)
		open_file_folder(file)


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