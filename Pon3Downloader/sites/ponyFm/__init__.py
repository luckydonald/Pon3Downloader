# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

from DictObject.encoding import to_unicode as u
from DictObject.encoding import to_binary as b
import eyed3
import re, os
from ...utilities.files import download_file, get_json, do_a_filename, guess_extension
from ...utilities.tagging import overwrite_if_not


regex = re.compile("^(?:https?://)?pony\.fm/((?:api/web/)?(?:tracks/)|t)(?P<songid>\d+)")#https://regex101.com/r/uV7qO6/2
api_url = "https://pony.fm/api/web/tracks/{songid}?log=false"

def can_load(url):
	m =regex.match(url)
	if m:
		song_id = m.group("songid")
		logger.info("found song {id}".format(id=song_id))
		return song_id
	else:
		return None

def download_song(song_id, requested_type="mp3", cover_as_file=False):
		### Prepare/Get Meta ###
		requested_type = u(requested_type)
		json = get_json(api_url.format(songid=song_id))


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
		file_path, file_mime = download_file(download_src, return_mime=True)
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
		if audiofile.tag.comments.get(u""):
			text = audiofile.tag.comments.get(u"").text
			text += u("\n-----\nDownloaded from https://pony.fm/ with Pon3Downloader (https://github.com/luckydonald/pon3downloader/).")
			audiofile.tag.comments.set(text)
		else:
			audiofile.tag.comments.set(u("Downloaded from https://pony.fm/ with Pon3Downloader (https://github.com/luckydonald/pon3downloader/)"))
		audiofile.tag.comments.set(u("https://github.com/luckydonald/pon3downloader"), u("Download"))
		audiofile.tag.comments.set(u("https://github.com/luckydonald/pon3downloader"), u("Downloader"))
		audiofile.tag.comments.set(u("https://pony.fm/"), u("Origin"))
		audiofile.tag.save()

		### COVER ART ###

		imageData, imageMine = download_file(json.track.covers.normal, return_mime=True, return_buffer=True)
		imageType = eyed3.id3.frames.ImageFrame.FRONT_COVER
		frame = audiofile.tag.images.set(imageType, imageData, b(imageMine))
		frame.description = u('https://bitbucket.org/nicfit/eyed3/issues/27#comment-18763468')

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
		return music_file_path








def tests():
	# TODO: Tests.
	# "https://pony.fm/tracks/2795-vinylz-eq-paradise" -> steam only
	# "https://pony.fm/tracks/2794-applejack-too-soon" -> mp3 DL
	pass