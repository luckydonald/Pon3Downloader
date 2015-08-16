# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

from luckydonaldUtils.encoding import to_unicode as u
from luckydonaldUtils.encoding import to_binary as b
import eyed3
import os
from luckydonaldUtils.download import download_file, get_json
from luckydonaldUtils.files import do_a_filename, guess_extension
from ...utilities.stuff import Plugin
from ...utilities.tagging import overwrite_if_not
from luckydonaldUtils.store import Store
from ... import IDENTIFIER

import re
import requests
from bs4 import BeautifulSoup
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X10.69; rv:4458.42) Gecko/4458 Firefox/69.0 Pon3Downloader'}
TOKEN_REGEX = re.compile('token:\s*"(?P<token>[a-zA-Z0-9]+)"')



URL_REGEX = re.compile("^(?:https?://)?pony\.fm/(www\.)?((?:api/web/)?(?:tracks/)|t)(?P<songid>\d+)")  # https://regex101.com/r/uV7qO6
API_URL = "https://pony.fm/api/web/tracks/{songid}?log=false"


class PonyFM(Plugin):
	@classmethod
	def can_load(self, url):
		m = URL_REGEX.match(url)
		if m:
			song_id = m.group("songid")
			logger.info("found song {id}".format(id=song_id))
			return song_id
		else:
			return None

	@classmethod
	def download_song(self, song_id, requested_type="mp3", cover_as_file=False):
			### Prepare/Get Meta ###
			requested_type = u(requested_type)
			if self and isinstance(self, PonyFM) and self.session:
				json = get_json(API_URL.format(songid=song_id), cookies=self.session.cookies)
			else:
				json = get_json(API_URL.format(songid=song_id))


			### FILE Download ###

			download_src = None
			if "formats" in json.track:
				for download_format in json.track.formats:
					logger.debug("Found {extension} download.".format(extension=download_format.extension))
					if u(download_format.extension) == requested_type:
						download_src = download_format.url
						logger.debug("Got what we need. Skipping rest.")
						break
					#end if
				#end for
			#end if
			if download_src is None:  # not found > try streams
				if int(json.track.is_downloadable) != 1:
					logger.warn("Song is marked as 'not downloadable'! The downloaded stream might be bad quality!")
				else:
					logger.warn("Did not found the requested download type, searching in the stream formats. They might be bad quality!")
				#end if
				for extension, url in json.track.streams.items():  # for python 2 this should use iteritems() ... but meh.
					logger.debug("Found {extension} stream.".format(extension=extension))
					if u(extension) == requested_type:
						logger.debug("Got what we need. Skipping rest.")
						download_src = url
						break
				else:  # neither dl, nor streams > ERROR!
					logger.error("Did not (at all) found requested type ({requested_type})!".format(requested_type=requested_type))
					raise AssertionError("Could not find download.")  # TODO: custom DL Exception
				#end for-else
			#end if
			assert(download_src is not None)
			if self and isinstance(self, PonyFM) and self.session:
				file_path, file_mime = download_file(download_src, return_mime=True, progress_bar=True, cookies=self.session.cookies)
			else:
				file_path, file_mime = download_file(download_src, return_mime=True, progress_bar=True)
			logger.info("Downloaded mp3 from '{url}' to '{path}'".format(url=download_src, path=file_path))

			if u(file_mime) not in [u("audio/mp3"),u("audio/mpeg")]:
				raise AssertionError("mp3 is not mp3..")  # TODO: custom exception
			else:
				extension = "mp3"

			### META ###

			audiofile = eyed3.load(file_path)
			if audiofile.tag is None:
				audiofile.initTag()
			artist = u(json.track.user.name)
			logger.debug("")
			if not audiofile.tag.title:
				logger.debug("Title was empty.")
				audiofile.tag.title = u(json.track.title)
			overwrite_if_not(audiofile.tag, "artist", artist)
			overwrite_if_not(audiofile.tag, "audio_file_url", u("https://github.com/luckydonald/pon3downloader/"))
			overwrite_if_not(audiofile.tag, "artist_url", u(json.track.user.url))
			overwrite_if_not(audiofile.tag, "genre", u(json.track.genre.name))
			overwrite_if_not(audiofile.tag, "lyrics", [u(json.track.lyrics)])
			overwrite_if_not(audiofile.tag, "audio_source_url", u(json.track.url))
			#if audiofile.tag.comments.get(u""):
			#	text = audiofile.tag.comments.get(u"").text
			#	text += u("\n-----\nDownloaded from https://pony.fm/ with Pon3Downloader (https://github.com/luckydonald/pon3downloader/).")
			#	audiofile.tag.comments.set(text)
			#else:
			audiofile.tag.comments.set(u("Downloaded from {track_url} with Pon3Downloader (https://github.com/luckydonald/pon3downloader/)".format(track_url = json.track.url)))
			audiofile.tag.comments.set(u("https://github.com/luckydonald/pon3downloader"), u("Downloader"))
			audiofile.tag.save()

			### COVER ART ###
			if self and isinstance(self, PonyFM) and self.session:
				imageData, imageMine = download_file(json.track.covers.normal, return_mime=True, return_buffer=True, progress_bar=True, cookies=self.session.cookies)
			else:
				imageData, imageMine = download_file(json.track.covers.normal, return_mime=True, return_buffer=True, progress_bar=True)
			imageType = eyed3.id3.frames.ImageFrame.FRONT_COVER
			audiofile.tag.images.set(imageType, imageData, b(imageMine), description=u(" "))
			### SAVE ###

			audiofile.tag.save()
			logger.debug("wrote file meta.")
			new_file_name = "{artist} - {title}".format(artist=artist,title=json.track.title)
			new_file_name = do_a_filename(new_file_name)
			music_file_name = new_file_name + "." + extension
			logger.info("Renaming to '{filename}'".format(filename=music_file_name))
			file_folder = os.path.dirname(file_path)
			music_file_path = os.path.join(file_folder, music_file_name)
			logger.debug("Full new path will be '{path}'.".format(path=music_file_path))
			os.rename(file_path, music_file_path)
			if cover_as_file:
				logger.debug("Trying also writing the cover file.")
				cover_file_name = new_file_name + guess_extension(imageMine)
				cover_file_path = os.path.join(file_folder, cover_file_name)
				with open(cover_file_path, mode="wb+") as cover_file:
					cover_file.write(imageData)

			### FAVE ###
			if json.track.user_data:
				if json.track.user_data.is_favourited == 0:
					if self and isinstance(self, PonyFM) and self.session and self.token:
						logger.debug("Favouriting it now.")
						self.toggle_fave(json.track.id)
					else:
						logger.debug("User is not logged in.")
				else:
					logger.info("Song already is favorite.")
			return music_file_path

	def __init__(self, username=None, password=None, key=None):
		self.username = username
		self.__password = password
		self.__key = key
		if self.username and self.__password:
			self.login()
			self.get_token()
		self.session = None
		self.token = None




	def set_credentials(self, username, password, key):
		self.username = username
		self.__password = password
		self.__key = key

	def login(self):
		if not self.username or not self.__password or not self.__key:
			raise AssertionError("Please set username/password with `.set_credentials(user, pass)` first.")
		session = requests.Session()
		poniverse_ponyfm_url="https://poniverse.net/oauth/authorize?%2Foauth%2Fauthorize&client_id=3&redirect_uri=https%3A%2F%2Fpony.fm%2Fauth%2Foauth&response_type=code&state=login"
		poniverse_start = 'https://poniverse.net/oauth/login'
		poniverse_login_url = 'https://poniverse.net/login'
		pony_fm_url = 'https://pony.fm'

		r = session.get(poniverse_ponyfm_url, headers=HEADERS, verify=False)
		assert (r.url == poniverse_start)
		token = BeautifulSoup(r.text).findAll(attrs={'name' : '_token'})[0].get('value').encode()
		payload = {'_token' : token,
				   'username' : self.username,
				   'password' : Store(IDENTIFIER, self.__key).decrypt(self.__password),
				   'checkbox' : '1',
				   'submit' : '',
				   }

		r = session.post(poniverse_login_url, data=payload, headers=HEADERS, verify=False, allow_redirects=True,cookies=session.cookies)
		if r.url == pony_fm_url: # XXX
			logger.info("Logged in")
		else:
			from luckydonaldUtils.interactions import confirm
			if confirm("Login failed. Reset password?", default=True):
				from ...utilities.settings import settings
				settings.ponyfm_user = ""
				settings.ponyfm_pass = ""
				settings.save_settings()
				import sys
				sys.exit(77)
			raise AssertionError("login failed")
		self.session = session
		return session

	def get_token(self):
		if not self.session:
			self.login()
		r = self.session.get('https://pony.fm', headers=HEADERS, verify=False, allow_redirects=True, cookies=self.session.cookies)
		bs = BeautifulSoup(r.text)
		script = [script for script in bs.findAll("script") if "token" in script.text][0]
		m = TOKEN_REGEX.search(str(script))
		if m:
			self.token = m.group(1)
			return self.token


	def toggle_fave(self, song_id):
		if not self.session:
			self.login()
		if not self.token:
			self.get_token()
		payload = {"type": "track", "id":str(song_id), "_token": self.token}
		r = self.session.post("https://pony.fm/api/web/favourites/toggle", data=payload, headers=HEADERS, verify=False, allow_redirects=True, cookies=self.session.cookies)
		return r










def tests():
	# TODO: Tests.
	# "https://pony.fm/tracks/2795-vinylz-eq-paradise" -> steam only
	# "https://pony.fm/tracks/2794-applejack-too-soon" -> mp3 DL
	# "https://pony.fm/i1728/normal.png" cover art url -> https://pony.fm/tracks/2736-sign-in-color-ponies-shying-from-dragons

	# "https://pony.fm/api/web/comments/track/2802": POST {"content":"Finally something so refreshingly different, but still Rainbow factory. Even if I really dislike Rainbow Factory (hate, even?), this song made it to my music collection on my hard drive. Awesome song!","_token":"3kYFkvHSVHHQTCnoZ1XtfITRVUO7eFvt7Bb4ouxT"}
	pass
