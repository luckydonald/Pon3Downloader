# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from setuptools import setup

long_description = """Downloads Music from pony.fm and eqbeat.org, filling in all the advanced ID3 meta tags, like lyrics and cover art."""

# http://peterdowns.com/posts/first-time-with-pypi.html
# $ python setup.py register -r pypi
# $ python setup.py sdist upload -r pypi

setup(
	name="pon3downloader",
	packages=['luckydonaldUtils'],
	version="0.2",
	author="luckydonald",
	author_email="code@luckydonald.de",
	description=long_description,
	license="BSD",
	keywords="download, music, ponies, DJ Pon3, pony.fm, eqbeats.org, Equestrian Beats, mp3, cover art images, "
			 "lyrics, ID3, pony, littlepip is best pony",
	url="https://github.com/luckydonald/pon3downloader/",
	install_requires=["DictObject", "requests", "eyeD3", "python-magic", "luckydonald-utils", 'usersettings', 'BeautifulSoup'],
	long_description=long_description,
	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Topic :: Utilities",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
	],
)


