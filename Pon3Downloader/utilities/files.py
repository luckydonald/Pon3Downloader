# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)


import requests
import tempfile
import hashlib
import mimetypes # get mime types/suffix for DL.
import magic
import os
import errno #exist_ok workaround
from DictObject import DictObject
from requests.packages.urllib3.exceptions import HTTPError

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X10.69; rv:4458.42) Gecko/4458 Firefox/69.0 Pon3Downloader'}



def gettempdir():
	temp_dir = tempfile.gettempdir()
	temp_dir = os.path.join(temp_dir, "pon3downloader")
	#py3
	# os.makedirs(temp_dir, exist_ok=True) #don't raise errors if existent.
	#py2/3 exist_ok workaround
	try:
		os.makedirs(temp_dir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	#end exist_ok workaround
	return temp_dir


def get_json(url, objectify=True):
	json = requests.get(url, headers=HEADERS, verify=False).json()
	if objectify:
		return DictObject.objectify(json)
	return json


def download_file(url, used_cached=True, temp_dir=None, return_mime=False, return_buffer=False):
	"""

	:param url:
	:param used_cached:
	:param temp_dir:
	:param return_mime:
	:param return_buffer: True: Don't write a file, just return the buffer. False: Write to file, return the files path
	:type  return_buffer: bool
	:return:
	"""
	if not return_buffer:
		if not temp_dir:
			temp_dir = gettempdir()
		file_name = url.split("/")[-1]
	#end if not return_buffer
	try:
		logger.debug("DL: Downloading from '{url}'.".format(url=url))
		#image_buffer = urlopen(url).read()
		image_buffer = requests.get(url, headers=HEADERS, verify=False).content


	except HTTPError as e:
		logger.exception("DL: Error in URL '" + url + "'.\n" + str(e))
		raise
		#return (None, None) if return_mime else None
	except Exception as e:
		logger.exception("DL: Error in Download '" + url + "'.\n" + str(e))
		raise
		#return (None, None) if return_mime else None
	mime = magic.from_buffer(image_buffer, mime=True).decode("utf-8")
	suffix = (mimetypes.guess_extension(mime) if mime else ".unknown") or ".unknown"
	if return_buffer:
		logger.debug("DL: Requested Buffer, not creating/checking dirs/files.")
		if return_mime:
			return image_buffer, mime
		return image_buffer
	else: # -> not return_buffer:
		file_name = str(hashlib.md5(url.encode()).hexdigest()) + suffix
		file_name = os.path.join(temp_dir, file_name)
		if os.path.isfile(file_name):
			if used_cached:
				logger.debug("DL: File exists, using cached: %s" % file_name)
				if return_mime:
					return file_name, mime
				return file_name
			logger.debug("DL: File exists, redownloading: %s" % file_name)
		else:
			logger.debug("DL: File does not exist, downloading: %s" % file_name)
			if not os.path.exists(os.path.dirname(file_name)):
				logger.debug("DL: Download Folder does not exists. Creating.")
				os.makedirs(os.path.dirname(file_name))
		logger.debug("DL: Writing download from '%s' to file '%s'" % (url, file_name))
		try:
			with open(file_name, 'wb') as f:
				f.write(image_buffer)
		except Exception as e:
			logger.error("DL: Error in writing download to disk: '" + url + "' to '" + file_name + "'.\n" + str(e))
			file_name = None
		if return_mime:
			return file_name, mime
		return file_name
	#end if-else
#end def


def get_file_suffix(file_path=None, file_url=None):
	mime = get_file_mime(file_path=file_path, file_url=file_url)
	return guess_extension(mime)


def guess_extension(mime):
	return mimetypes.guess_extension(type=mime or "")


def get_file_mime(file_path=None, file_url=None):
		if file_url:
			url = file_url
		elif file_path:
			from urllib.request import pathname2url
			url = pathname2url(file_path)
		else:
			raise AttributeError("Neither URL (file_url) nor local path (file_path) given.")
		mime = magic.from_file(file_path).decode("utf-8")
		return mime

def do_a_filename(input_file_name):
	output_file_name = input_file_name
	for replacer in [(":",""), ("?",""), ("*",""), ("”","\""),(">",""), ("<",""), ("|","-"), ("\\"," "), ("/"," ")]:
		output_file_name = output_file_name.replace(replacer[0], replacer[1])
	logger.debug("Filename '{old_filename}' is now '{new_filename}'.".format(old_filename=input_file_name, new_filename=output_file_name))
	return output_file_name


import subprocess
import sys

"""
def open_folder(folder_path)
"""  # for different Platforms
if sys.platform == 'darwin':  # Mac OS
	def open_folder(folder_path):
		subprocess.check_call(['open', '--', folder_path])
	def open_file_folder(folder_path):
		subprocess.check_call(['open', '-R', '--', folder_path])
elif sys.platform == 'linux2':  # linux, hopefully has gnome?
	def open_folder(folder_path):
		subprocess.check_call(['gnome-open', '--', folder_path])  # untested.
	def open_file_folder(file_path):
		open_folder(os.path.dirname(file_path))
elif sys.platform == 'win32':  # windows
	def open_folder(folder_path):
		subprocess.check_call(['explorer', folder_path])
	def open_file_folder(file_path):
		try:
			subprocess.check_call(['explorer', '/select,"%s"' % file_path])
		except:
			open_folder(os.path.dirname(file_path))
